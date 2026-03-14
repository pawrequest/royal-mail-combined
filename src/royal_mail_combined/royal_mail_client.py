from datetime import date

from royal_mail_combined.all_models import (
    AvailableServicesResponse,
    ReturnsRequest,
    ReturnsResponse,
)
from royal_mail_combined.click_and_drop_api.client import ClickAndDropClient
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.endpoints import RETURNS_ENDPOINT, RETURNS_SERVICES_ENDPOINT
from royal_mail_combined.core.http_client import BaseHttpClient
from royal_mail_combined.parcels_apis.client import ParcelAPIClient
from royal_mail_combined.parcels_apis.collection_order.models import (
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


class RMHttpClient(BaseHttpClient):
    def _book_inbound_shipment_single(self, return_request: ReturnsRequest) -> ReturnsResponse:
        res = self.do_post(
            url=RETURNS_ENDPOINT,
            data=return_request,
            headers=self.settings.authorised_headers_bearer(),
        )
        res_model = ReturnsResponse.model_validate(res.json())
        return res_model

    def book_inbound_shipment(
        self, return_request: ReturnsRequest, num_boxes: int = 1
    ) -> list[ReturnsResponse]:
        return [self._book_inbound_shipment_single(return_request) for _ in range(num_boxes)]

    def check_return_services(self) -> AvailableServicesResponse:
        # WARNING ServiceNames returned from here are not correct for use with CollectionsOrderCreate endpoint - must hardcode values from support email
        res = self.do_get(
            url=RETURNS_SERVICES_ENDPOINT, headers=self.settings.authorised_headers_bearer()
        )
        res_model = AvailableServicesResponse.model_validate(res.json())
        return res_model


class RoyalMailClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        self.settings = settings
        self.http_client = RMHttpClient(settings=settings)
        self.click_and_drop = ClickAndDropClient(settings=settings)
        self.parcel_api = ParcelAPIClient(settings=settings)

        # Create
        self.book_outbound_shipment = self.click_and_drop.book_shipment
        self.book_inbound_shipment = self.http_client.book_inbound_shipment

        # Read
        self.fetch_orders = self.click_and_drop.orders_api.get_orders_async
        self.fetch_specific_orders = self.click_and_drop.orders_api.get_specific_orders_async
        self.address_search = self.parcel_api.address_search
        self.address_retrieve = self.parcel_api.address_api.address_retrieve
        self.address_verify = self.parcel_api.address_api.address_verify

        # Delete
        self.cancel_outbound_shipment = self.click_and_drop.orders_api.delete_orders_async
        # self.cancel_inbound_shipment = #  good luck with that. call your account manager and complain about lack of cancel endpoint in returns API (and ask them to cancel the label).
        self.cancel_collection = self.parcel_api.cancel_collection

    def book_inbound_shipment_with_collection(
        self,
        return_request: ReturnsRequest,
        collection_date: date,
        num_boxes: int,
        box_dims: DimensionsPostDef = DimensionsPostDef.large(),
        box_weight_kg: int = 8,
    ) -> CollectionOrderCreateResponse:
        # gather shipment data
        sender_address_verified = self.parcel_api.verify_return_address(
            return_request.shipment.sender_address
        )
        dps = sender_address_verified.dps
        postcode_and_dps = sender_address_verified.input.postcode.replace(' ', '') + dps
        collection_address = AddressMandatoryDef(
            **sender_address_verified.input.model_dump(), dps=dps
        )

        # book shipping
        booking_responses = self.book_inbound_shipment(return_request, num_boxes=num_boxes)

        # gather collection data
        items = [
            ItemsPostDef(
                item_barcode_id=booking_response.shipment.tracking_number,
                weight_in_grams=1000 * box_weight_kg,
                item_service_name='Tracked Returns 24 (T24) Enhanced',
                item_type=CollectionItemType.STANDARD,
                dimensions=box_dims,
            )
            for booking_response in booking_responses
        ]

        # book collection
        token = self.parcel_api.get_token(collection_date, num_boxes, postcode_and_dps)
        collection = CollectionMandatory(
            timeslot_reservation_id=token,
            sender_details=return_request.shipment.sender_address.details,
            account_details=self.settings.account_details,
            address=collection_address,
            collection_date=collection_date,
            items=items,
        )

        return self.parcel_api.collection_orders_api.order_create_mandatory(collection=collection)
