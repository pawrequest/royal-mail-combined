from royal_mail_combined.click_and_drop.orders import DeleteOrdersResource
from royal_mail_combined.click_and_drop.responses import CreateOrdersResponse
from royal_mail_combined.clients._base_client import _RMBaseClient
from royal_mail_combined.click_and_drop.models import CreateOrderRequestContainer
from royal_mail_combined.clients.exceptions import raise_for_rm_status

BASE_URL = r'https://api.parcel.royalmail.com/api/v1'


class ClickAndDropClient(_RMBaseClient):
    def create_order(self, orders: CreateOrderRequestContainer) -> CreateOrdersResponse:
        url = BASE_URL + r'/orders'
        res = self._do_post(url=url, data=orders, headers=self.settings.headers_bearer()).json()
        return CreateOrdersResponse.model_validate(res)

    def cancel_shipment(self, order_ident: str | int) -> DeleteOrdersResource:
        ident = str(order_ident)
        url = BASE_URL + r'/orders/' + ident
        res = self._do_delete(url=url, headers=self.settings.headers_bearer()).json()
        return DeleteOrdersResource.model_validate(res)

