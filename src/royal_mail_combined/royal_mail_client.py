from datetime import date

from royal_mail_combined.all_models import (
    AvailableServicesResponse,
    ReturnsRequest,
    ReturnsResponse,
)
from royal_mail_combined.click_and_drop_api.client import ClickAndDropClient
from royal_mail_combined.click_and_drop_api.models.return_models import ReturnRequestContainer, ReturnResponseContainer
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.endpoints import RETURNS_ENDPOINT, RETURNS_SERVICES_ENDPOINT
from royal_mail_combined.core.http_client import BaseHttpClient
from royal_mail_combined.parcels_apis.address.models.address import AddressDps
from royal_mail_combined.parcels_apis.client import ParcelAPIClient
from royal_mail_combined.parcels_apis.collection_order.models import (
    CollectionMandatory,
    DimensionsPostDef,
    ItemsPostDef,
)


class RMHttpClient(BaseHttpClient):
    """Manually implemented Http calls"""

    def _book_inbound_shipment_single(self, return_request: ReturnsRequest) -> ReturnsResponse:
        res = self.do_post(
            url=RETURNS_ENDPOINT,
            data=return_request,
            headers=self.settings.authorised_headers_bearer(),
        )
        res_model = ReturnsResponse.model_validate(res.json())
        return res_model

    def book_inbound_shipment_no_conrtainer(
        self, return_request: ReturnsRequest, num_boxes: int = 1
    ) -> ReturnResponseContainer:
        return ReturnResponseContainer(
            created_orders=[self._book_inbound_shipment_single(return_request) for _ in range(num_boxes)]
        )

    def book_inbound_shipment(self, return_request_container: ReturnRequestContainer) -> ReturnResponseContainer:
        return ReturnResponseContainer(
            created_orders=[self._book_inbound_shipment_single(_) for _ in return_request_container.return_requests]
        )

    def check_return_services(self) -> AvailableServicesResponse:
        """WARNING ServiceNames returned from here are not correct for use with CollectionsOrderCreate endpoint - must hardcode values from ReturnsServiceNames Enum"""
        res = self.do_get(url=RETURNS_SERVICES_ENDPOINT, headers=self.settings.authorised_headers_bearer())
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
        self.get_label_data = self.click_and_drop.labels_api.get_orders_label_async

        # Delete
        self.cancel_outbound_shipment = self.click_and_drop.orders_api.delete_orders_async
        # self.cancel_inbound_shipment = #  good luck with that. call your account manager and complain about lack of cancel endpoint in returns API (and ask them to cancel the label).
        self.cancel_collection = self.parcel_api.cancel_collection

    def book_inbound_shipment_with_collection(
        self,
        return_request_container: ReturnRequestContainer,
        collection_date: date,
        box_dims: DimensionsPostDef = DimensionsPostDef.large(),
        box_weight_kg: int = 8,
    ) -> ReturnResponseContainer:
        # gather shipment data
        sender_address_verified = self.parcel_api.verify_return_address(
            return_request_container.return_requests[0].shipment.sender_address
        )
        dps = sender_address_verified.dps
        postcode_and_dps = sender_address_verified.input.postcode.replace(" ", "") + dps
        collection_address = AddressDps(**sender_address_verified.input.model_dump(exclude_none=True), dps=dps)

        # book shipping
        booking_response_container = self.book_inbound_shipment(return_request_container)

        # gather collection data
        items = [
            ItemsPostDef.tracked_24_return_standard(booking_response.shipment.tracking_number, box_weight_kg, box_dims)
            for booking_response in booking_response_container.created_orders
        ]

        # book collection
        token = self.parcel_api.get_token(collection_date, len(items), postcode_and_dps)
        collection = CollectionMandatory(
            timeslot_reservation_id=token,
            sender_details=return_request_container.return_requests[0].shipment.sender_address.details,
            account_details=self.settings.account_details,
            address=collection_address,
            collection_date=collection_date,
            items=items,
        )
        collection_resp = self.parcel_api.collection_orders_api.order_create_mandatory(collection=collection)

        booking_response_container.collection_response = collection_resp
        return booking_response_container

    # def book_inbound_shipment_with_collection_no_container(
    #     self,
    #     return_request: ReturnsRequest,
    #     collection_date: date,
    #     num_boxes: int,
    #     box_dims: DimensionsPostDef = DimensionsPostDef.large(),
    #     box_weight_kg: int = 8,
    # ) -> ReturnResponseContainer:
    #     # gather shipment data
    #     sender_address_verified = self.parcel_api.verify_return_address(return_request.shipment.sender_address)
    #     dps = sender_address_verified.dps
    #     postcode_and_dps = sender_address_verified.input.postcode.replace(" ", "") + dps
    #     collection_address = AddressDps(**sender_address_verified.input.model_dump(exclude_none=True), dps=dps)
    #
    #     # book shipping
    #     return_request_container = ReturnRequestContainer(return_requests=[return_request for _ in range(num_boxes)])
    #     booking_response_container = self.book_inbound_shipment(return_request_container, num_boxes=num_boxes)
    #
    #     # gather collection data
    #     items = [
    #         ItemsPostDef.tracked_24_return_standard(booking_response.shipment.tracking_number, box_weight_kg, box_dims)
    #         for booking_response in booking_response_container.created_orders
    #     ]
    #
    #     # book collection
    #     token = self.parcel_api.get_token(collection_date, num_boxes, postcode_and_dps)
    #     collection = CollectionMandatory(
    #         timeslot_reservation_id=token,
    #         sender_details=return_request.shipment.sender_address.details,
    #         account_details=self.settings.account_details,
    #         address=collection_address,
    #         collection_date=collection_date,
    #         items=items,
    #     )
    #     collection_resp = self.parcel_api.collection_orders_api.order_create_mandatory(collection=collection)
    #
    #     booking_response_container.collection_response = collection_resp
    #     return booking_response_container
