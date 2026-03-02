from datetime import datetime

from royal_mail_combined.apis.parcels_apis.address.models import (
    AddressFindRequestDef,
    AddressRecordDef,
    AddressSummaryDef,
    AddressVerifyReqRespdef,
    AddressVerifyRequestDef,
)
from royal_mail_combined.apis.click_and_drop.models import (
    CreateOrdersRequest,
    CreateOrdersResponse,
    DeleteOrdersResource,
    GetOrdersResponse,
)
from royal_mail_combined.apis.parcels_apis.collection_handler.models import GetAvailableSlotsResponse
from royal_mail_combined.apis.parcels_apis.collection_order.models import Collection
from royal_mail_combined.apis.returns.models import ReturnsRequest, ReturnsResponse
from royal_mail_combined.core.endpoints import (
    ADDRESS_BASE,
    CAD_ORDERS,
    COLLECTION_HANDLER_NET,
    CAD_COLLECTION_ORDER,
    COLLECTION_ORDER_CREATE,
    DELIVERY_OFFICE_BASE,
    RETURNS_ENDPOINT,
)
from royal_mail_combined.core.http_client import RMBaseClient


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            print(f'Error in {func.__name__}: {e}')
            raise e

    return wrapper


class RoyalMailClient(RMBaseClient):
    # ORDERS
    @handle_errors
    def orders_fetch(
            self,
            page_size: int | None = None,
            start_date_time: datetime | None = None,
            end_date_time: datetime | None = None,
            continuation_token: str | None = None
    ) -> GetOrdersResponse:
        params = {
            'pageSize': page_size,
            'startDateTime': start_date_time.isoformat() if start_date_time else None,
            'endDateTime': end_date_time.isoformat() if end_date_time else None,
            'continuationToken': continuation_token
        }
        res = self.do_get(
            url=CAD_ORDERS,
            headers=self.settings.headers_bearer(),
            params=params
        )
        res_model = GetOrdersResponse.model_validate(res.json())
        return res_model

    def order_create(self, orders: CreateOrdersRequest) -> CreateOrdersResponse:
        res = self.do_post(url=CAD_ORDERS, data=orders, headers=self.settings.headers_bearer())
        res_model = CreateOrdersResponse.model_validate(res.json())
        return res_model

    def order_cancel(self, order_ident: str | int) -> DeleteOrdersResource:
        ident = str(order_ident)
        url = CAD_ORDERS + f'/{ident}'
        res = self.do_delete(url=url, headers=self.settings.headers_bearer())
        res_model = DeleteOrdersResource.model_validate(res.json())
        return res_model

    def order_create_return(self, return_request: ReturnsRequest | dict):
        res = self.do_post(url=RETURNS_ENDPOINT, data=return_request, headers=self.settings.headers_bearer())
        res_model = ReturnsResponse.model_validate(res.json())
        return res_model

    # ADDRESS
    def address_fetch(self, address_id: str) -> AddressRecordDef:
        res = self.do_get(url=f'{ADDRESS_BASE}/address/{address_id}')
        res_model = AddressRecordDef.model_validate(res.json())
        return res_model

    def address_search(self, address_search_str: str) -> list[AddressSummaryDef]:
        addr_search = AddressFindRequestDef(address_text=address_search_str)
        res = self.do_post(url=f'{ADDRESS_BASE}/address', data=addr_search)
        res_model = [AddressSummaryDef.model_validate(_) for _ in res.json()['addresses']]
        return res_model

    def address_search_dps(self, address_search: AddressVerifyRequestDef | dict) -> list[AddressVerifyReqRespdef]:
        res = self.do_post(url=f'{ADDRESS_BASE}/address/dps', data=address_search)
        res_model = [AddressVerifyReqRespdef.model_validate(_) for _ in res.json()]
        return res_model

    # COLLECTION
    def collection_create(self, data: Collection | dict) -> CreateOrdersResponse:
        res = self.do_post(url=COLLECTION_ORDER_CREATE, data=data)
        res_model = CreateOrdersResponse.model_validate(res.json())
        return res_model

    def collection_get(self, collection_id: str):
        url = CAD_COLLECTION_ORDER + f'/{collection_id}'
        res = self.do_get(url=url)
        res = res.json()
        return res

    def collection_cancel(self, collection_id: str):
        url = CAD_COLLECTION_ORDER + f'/{collection_id}'
        params = {'status': 'Cancelled'}
        res = self.do_put(url=url, data=params)
        res = res.json()
        return res

    def collection_slots_fetch(self, dps: str, item_count: int | str) -> GetAvailableSlotsResponse:
        params = {'dps': dps, 'itemCount': item_count}
        res = self.do_get(url=COLLECTION_HANDLER_NET + r'/slots', params=params)
        res_model = GetAvailableSlotsResponse.model_validate(res.json())
        return res_model

    def collection_subscription_check(self, barcode, family_name, account_number):
        params = {
            'productFamily': {
                "barcode": barcode,
                "productFamilyName": family_name,
                "accountNumber": account_number
            }
        }
        res = self.do_post(url=(COLLECTION_HANDLER_NET + r'/productfamily/subscription'), data=params)
        return res

    # DELIVERY OFFICE
    def delivery_office_get(self, postcode: str):
        params = {'postcode': postcode.replace(' ', '')}
        res = self.do_get(url=DELIVERY_OFFICE_BASE, params=params)
        raise NotImplementedError('Not Authorised how did you get here?')

    # DOCUMENTS
    def label_data_fetch(self, order_idents: str):
        url = CAD_ORDERS + f'/{order_idents}/label'
        # url = f'/orders/{order_idents}/label'

        params = dict(
            order_identifiers=order_idents,
            document_type='postageLabel',
            include_returns_label=False,
            include_cn=False,
        )
        res = self.do_get(url=url, params=params)
        res_model = res.json()
        return res_model
