from pprint import pprint, pformat

from loguru import logger

from royal_mail_combined.build_client import build_client
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.converters import add_label_gen_request
from royal_mail_combined.core.endpoints import CAD_BASE
from royal_mail_combined.core.exceptions import ApiException
from royal_mail_combined.apis.click_and_drop.api import LabelsApi, ManifestsApi, OrdersApi, VersionApi
from royal_mail_combined.apis.click_and_drop.models import (
    CreateOrderRequest,
    CreateOrdersRequest,
    CreateOrdersResponse,
)


def failed_order_errors(response):
    errors = [
        f'Error in {error.fields}: {error.error_code} - {error.error_message}'
        for fail in response.failed_orders
        for error in fail.errors
    ]
    if errors:
        pprint(errors, indent=4, width=120)
        raise ApiException('\n'.join(errors))


class ClickAndDropClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        client = build_client(settings=settings, host=CAD_BASE)
        self._version_api = VersionApi(client)
        self.fetch_version = self._version_api.get_version_async

        self.orders_api = OrdersApi(client)
        self.fetch_orders = self.orders_api.get_orders_async
        self.fetch_specific = self.orders_api.get_specific_orders_async
        self.delete_orders = self.orders_api.delete_orders_async

        self.labels_api = LabelsApi(client)
        self.fetch_label_data = self.labels_api.get_orders_label_async

        self.manifests_api = ManifestsApi(client)
        self.do_manifest = self.manifests_api.manifest_eligible_async

    # def book_shipment1(self, orders: CreateOrdersRequest, with_label: bool = True) -> CreateOrdersResponse:
    #     if with_label:
    #         add_label_gen_request(orders)
    #     try:
    #         response = self.orders_api.create_orders_async(create_orders_request=orders)
    #         failed_order_errors(response)
    #     except Exception as e:
    #         print(f'Exception when calling OrdersApi->create_orders_async: {e}\n')
    #         raise e
    #     return response

    def book_shipment(self, *orders: CreateOrderRequest, with_label: bool = True) -> CreateOrdersResponse:
        orders = list(orders)
        for order in orders:
            if with_label:
                add_label_gen_request(order)
        try:
            create_orders = CreateOrdersRequest(items=orders)
            response = self.orders_api.create_orders_async(create_orders_request=create_orders)
            astr = response.model_dump(exclude={'created_orders': {'__all__': {'label', 'qr_code'}}})
            logger.info(f'Booked orders response: {pformat(astr, indent=4, width=120)}')
            failed_order_errors(response)
        except Exception as e:
            print(f'Exception when calling OrdersApi->create_orders_async: {e}\n')
            raise e
        return response
