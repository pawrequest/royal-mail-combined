from datetime import date

from royal_mail_combined.all_models import AvailableServicesResponse, ReturnsRequest, ReturnsResponse
from royal_mail_combined.click_and_drop_api.client import ClickAndDropClient
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.converters import address_angonstic_to_verify_def
from royal_mail_combined.core.endpoints import RETURNS_ENDPOINT, RETURNS_SERVICES_ENDPOINT
from royal_mail_combined.core.http_client import RMBaseClient
from royal_mail_combined.parcels_apis.address.models import AddressVerifyRequestDef
from royal_mail_combined.parcels_apis.client import ParcelAPIClient
from royal_mail_combined.parcels_apis.collection_order.models import (
    AccountDetailsDef,
    AddressMandatoryDef,
    CollectionItemType,
    CollectionMandatory,
    CollectionOrderCreateResponse,
    DimensionsPostDef,
    ItemsPostDef,
)


def make_item(barcode_id: str, box_weight_kg: int, dims: DimensionsPostDef) -> ItemsPostDef:
    return ItemsPostDef(
        item_barcode_id=barcode_id,
        weight_in_grams=1000 * box_weight_kg,
        item_service_name='Tracked Returns 24 (T24) Enhanced',
        item_type=CollectionItemType.STANDARD,
        dimensions=dims,
    )


class RoyalMailClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        self.settings = settings
        self.http_client = RMBaseClient(settings=settings)
        self.click_and_drop = ClickAndDropClient(settings=settings)
        self.parcel_api = ParcelAPIClient(settings=settings)

    # ORDERS
    def book_return_shipment_order(self, return_request: ReturnsRequest) -> ReturnsResponse:
        # todo move this to ParcelApi?
        res = self.http_client.do_post(
            url=RETURNS_ENDPOINT, data=return_request, headers=self.settings.authorised_headers_bearer()
        )
        res_model = ReturnsResponse.model_validate(res.json())
        return res_model

    def book_return_with_collection(
        self,
        return_request: ReturnsRequest,
        collection_date: date,
        num_boxes: int,
        box_dims: DimensionsPostDef = None,
        box_weight_kg: int = None,
    ) -> CollectionOrderCreateResponse:
        box_weight_kg = box_weight_kg or 8
        dims = box_dims or DimensionsPostDef(height=30, width=30, depth=60)

        # get DPS
        sender_address_verify = address_angonstic_to_verify_def(return_request.shipment.sender_address)
        dps_request = AddressVerifyRequestDef(addresses=[sender_address_verify])
        dps_responses = self.parcel_api.address_verify(dps_request)
        sender_address_verified = dps_responses[0]
        dps = sender_address_verified.dps

        postcode_and_dps = sender_address_verified.input.postcode.replace(' ', '') + dps
        token = self.parcel_api.get_token(collection_date, num_boxes, postcode_and_dps)

        items = []
        for i in range(num_boxes):
            booking_response = self.book_return_shipment_order(return_request)
            barcode_id = booking_response.shipment.tracking_number
            items.append(make_item(barcode_id, box_weight_kg, dims))

        # book collection
        collection_address = AddressMandatoryDef(**sender_address_verified.input.model_dump(), dps=dps)
        collection = CollectionMandatory(
            timeslot_reservation_id=token,
            sender_details=return_request.shipment.sender_address.details,
            account_details=AccountDetailsDef(retailer_account_number=self.settings.account_number),
            address=collection_address,
            collection_date=collection_date,
            items=items,
        )

        return self.parcel_api.collection_create_mandatory(collection=collection)

    def check_return_services(self) -> AvailableServicesResponse:
        # ServiceNames returned from here are not correct for use with CollectionsOrderCreate endpoint
        res = self.http_client.do_get(url=RETURNS_SERVICES_ENDPOINT, headers=self.settings.authorised_headers_bearer())
        res_model = AvailableServicesResponse.model_validate(res.json())
        return res_model
