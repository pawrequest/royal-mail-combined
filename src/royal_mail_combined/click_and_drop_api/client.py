from pprint import pformat, pprint

from loguru import logger

from royal_mail_combined.click_and_drop_api.api import (
    LabelsApi,
    ManifestsApi,
    OrdersApi,
    VersionApi,
)
from royal_mail_combined.click_and_drop_api.models import (
    CreateOrderRequest,
    CreateOrdersRequest,
    CreateOrdersResponse,
)
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.build_client import build_client
from royal_mail_combined.core.endpoints import CAD_BASE
from royal_mail_combined.core.exceptions import ApiException


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
        self.version_api = VersionApi(client)
        self.orders_api = OrdersApi(client)
        self.labels_api = LabelsApi(client)
        self.manifests_api = ManifestsApi(client)

    def book_shipment(self, order: CreateOrderRequest, with_label: bool = True) -> CreateOrdersResponse:
        # if with_label:
        #     order.add_label_request()
        try:
            create_orders = CreateOrdersRequest(items=[order])
            response = self.orders_api.create_orders_async(create_orders_request=create_orders)
            astr = response.model_dump(exclude={'created_orders': {'__all__': {'label', 'qr_code'}}})
            logger.info(f'Booked orders response: {pformat(astr, indent=4, width=120)}')
            failed_order_errors(response)
        except Exception as e:
            print(f'Exception when calling OrdersApi->create_orders_async: {e}\n')
            raise e
        return response
