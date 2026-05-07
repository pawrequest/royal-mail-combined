from datetime import date

from loguru import logger

from royal_mail_combined.all_models import (
    AvailableServicesResponse,
    ReturnsRequest,
    ReturnsResponse,
)
from royal_mail_combined.click_and_drop_api.client import ClickAndDropClient
from royal_mail_combined.click_and_drop_api.models import ReturnsResponse
from royal_mail_combined.click_and_drop_api.models.return_models import (
    AddressReturns,
    ReturnRequestContainer,
    ReturnResponseContainer,
)
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.converters import details_from_address
from royal_mail_combined.core.endpoints import RETURNS_ENDPOINT, RETURNS_SERVICES_ENDPOINT
from royal_mail_combined.core.http_client import BaseHttpClient
from royal_mail_combined.parcels_apis.address.models.address import AddressDps
from royal_mail_combined.parcels_apis.client import ParcelAPIClient
from royal_mail_combined.parcels_apis.collection_order.models import (
    CollectionMandatory,
    CollectionOrderCreateResponse,
    DimensionsPostDef,
    ItemsPostDef,
    SenderDetailsPostDef,
)


class RMHttpClient(BaseHttpClient):
    """Manually implemented Http calls"""

    def _book_inbound_shipment_single(self, return_request: ReturnsRequest) -> ReturnsResponse:
        logger.info('Booking inbound shipment with Royal Mail')
        res = self.do_post(
            url=RETURNS_ENDPOINT,
            data=return_request,
            headers=self.settings.authorised_headers_bearer(),
        )
        res_json = res.json()
        # logmsg = pprint.pformat(res_json, indent=2, width=120)
        logger.info(f'Response status from booking inbound collection: {str(res)}')
        res_model = ReturnsResponse.model_validate(res_json)
        logger.info(
            f'Booked inbound shipment with Royal Mail, tracking number: '
            f'{res_model.shipment.tracking_number}, unique_id = {res_model.shipment.unique_item_id}'
        )
        return res_model

    def book_inbound_shipment(self, return_request_container: ReturnRequestContainer) -> ReturnResponseContainer:
        return ReturnResponseContainer(
            created_orders=[self._book_inbound_shipment_single(_) for _ in return_request_container.return_requests]
        )

    def check_return_services(self) -> AvailableServicesResponse:
        """WARNING ServiceNames returned from here are not correct for use with CollectionsOrderCreate endpoint - must hardcode values from ReturnsServiceNames Enum"""
        res = self.do_get(url=RETURNS_SERVICES_ENDPOINT, headers=self.settings.authorised_headers_bearer())
        res_model = AvailableServicesResponse.model_validate(res.json())
        return res_model


def build_items(
    box_dims: DimensionsPostDef, box_weight_kg: int, success_orders: list[ReturnsResponse]
) -> list[ItemsPostDef]:
    items = [
        ItemsPostDef.tracked_24_return_standard(booking_response.shipment.tracking_number, box_weight_kg, box_dims)
        for booking_response in success_orders
    ]
    return items


class RoyalMailClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        self.settings = settings
        self.http_client = RMHttpClient(settings=settings)
        self.click_and_drop = ClickAndDropClient(settings=settings)
        self.parcel_api = ParcelAPIClient(settings=settings)

        # Create
        self.book_outbound = self.click_and_drop.book_shipments
        self.book_inbound_shipping = self.http_client.book_inbound_shipment

        # Read
        self.fetch_orders = self.click_and_drop.orders_api.get_orders_async
        self.fetch_specific_orders = self.click_and_drop.orders_api.get_specific_orders_async
        self.address_search = self.parcel_api.address_search
        self.address_retrieve = self.parcel_api.address_api.address_retrieve
        self.address_verify = self.parcel_api.address_api.address_verify
        self.get_label_data = self.click_and_drop.labels_api.get_orders_label_async

        # Delete
        self.cancel_outbound_shipment = self.click_and_drop.orders_api.delete_orders_async
        # self.cancel_inbound_shipment = #  good luck with that. call your account manager and complain about
        # lack of cancel endpoint in returns API (and ask them to cancel the label).
        self.cancel_collection = self.parcel_api.cancel_collection

    def book_inbound_with_collection(
        self,
        return_request_container: ReturnRequestContainer,
        collection_date: date,
        box_dims: DimensionsPostDef = DimensionsPostDef.large(),
        box_weight_kg: int = 8,
    ) -> ReturnResponseContainer:
        booking_response_container = self.book_inbound_shipping(return_request_container)

        success_orders = booking_response_container.created_orders
        items = build_items(box_dims, box_weight_kg, success_orders)

        collection_address = return_request_container.return_requests[0].shipment.sender_address
        collection_resp = self._book_collection_only(
            collection_address=collection_address,
            collection_date=collection_date,
            items=items,
        )

        booking_response_container.collection_response = collection_resp
        return booking_response_container

    def book_inbound_with_collection_if_can_collect(
        self,
        return_request_container: ReturnRequestContainer,
        collection_date: date,
        box_dims: DimensionsPostDef = DimensionsPostDef.large(),
        box_weight_kg: int = 8,
    ) -> ReturnResponseContainer:

        # gather shipment data
        collection_address_verified = self.parcel_api.verify_return_address(
            return_request_container.return_requests[0].shipment.sender_address
        )
        postcode_and_dps = collection_address_verified.input.postcode.replace(' ', '') + collection_address_verified.dps

        token = self.get_collection_token(
            collection_date, len(return_request_container.return_requests), postcode_and_dps
        )
        if not token:
            raise ValueError('No collection token available for the given date and items, cannot book collection')
        booking_response_container = self.book_inbound_shipping(return_request_container)

        success_orders = booking_response_container.created_orders
        items = build_items(box_dims, box_weight_kg, success_orders)

        collection_address = return_request_container.return_requests[0].shipment.sender_address
        collection_resp = self._book_collection_only(
            collection_address=collection_address,
            collection_date=collection_date,
            items=items,
        )

        booking_response_container.collection_response = collection_resp
        return booking_response_container

    def _book_collection_only(
        self,
        collection_address: AddressReturns,
        collection_date: date,
        items: list[ItemsPostDef],
    ) -> CollectionOrderCreateResponse:
        logger.info('Booking inbound collection with Royal Mail')

        # gather shipment data
        collection_address_verified = self.parcel_api.verify_return_address(collection_address)
        dps = collection_address_verified.dps
        postcode_and_dps = collection_address_verified.input.postcode.replace(' ', '') + dps
        collection_address_dps = AddressDps(**collection_address_verified.input.model_dump(exclude_none=True), dps=dps)

        # fetch collection token and build collection request
        token = self.get_collection_token(collection_date, len(items), postcode_and_dps)
        collection = CollectionMandatory(
            timeslot_reservation_id=token,
            sender_details=SenderDetailsPostDef(
                sender_name=collection_address.full_name, sender_email=collection_address.email
            ),
            account_details=self.settings.account_details,
            address=collection_address_dps,
            collection_date=collection_date,
            items=items,
        )
        # book collection
        collection_resp = self.parcel_api.collection_orders_api.order_create_mandatory(collection=collection)
        return collection_resp

    def get_collection_token(self, collection_date: date, num_boxes: int, postcode_and_dps: str) -> str | None:
        token = self.parcel_api.get_token(collection_date, num_boxes, postcode_and_dps)
        return token
