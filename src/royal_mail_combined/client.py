from datetime import datetime
from pprint import pprint

import httpx
from pydantic import BaseModel

from royal_mail_combined.models.address import (
    AddressFindDPSRequest,
    AddressFindDPSResponse,
    AddressFindRequest,
    AddressRecord,
    AddressSummary,
)
from royal_mail_combined.models.exceptions import raise_for_rm_status
from royal_mail_combined.config import RMSettings
from royal_mail_combined.models.collections import Collection, GetAvailableSlotsResponse
from royal_mail_combined.models.orders import DeleteOrdersResource
from royal_mail_combined.models.responses import CreateOrdersResponse, GetOrdersResponse
from royal_mail_combined.models.click_and_drop import CreateOrderRequestContainer
from royal_mail_combined.models.returns import RETURNS_ENDPOINT, ReturnsRequest, ReturnsResponse

COLLECTION_HANDLER_BASE = r'https://api.royalmail.net/collectionorders/v1'
ADDRESS_BASE_URL = r'https://api.royalmail.net/addressfind/v1'
BASE_URL = r'https://api.parcel.royalmail.com/api/v1'
ORDERS_ENDPOINT = BASE_URL + r'/orders'
CREATE_URL = r'https://api.royalmail.net/orders/v1/collectionOrder/create'


class _RMBaseClient:
    def __init__(self, settings: RMSettings):
        self.settings = settings

    def _do_post(
            self,
            *,
            url: str,
            data: dict | BaseModel | None = None,
            headers: dict | None = None,
    ) -> httpx.Response:
        headers = headers or self.settings.headers()
        if isinstance(data, BaseModel):
            data = data.model_dump(mode='json', by_alias=True)
        res = httpx.post(url, headers=headers, json=data, timeout=30)
        raise_for_rm_status(res)
        return res

    def _do_get(
            self,
            *,
            url: str,
            params: BaseModel | dict | None = None,
            headers: dict | None = None,
    ) -> httpx.Response:
        headers = headers or self.settings.headers()
        if isinstance(params, BaseModel):
            params = params.model_dump(mode='json', by_alias=True)
        res = httpx.get(url, headers=headers, params=params, timeout=30)
        raise_for_rm_status(res)
        return res

    def _do_delete(
            self,
            *,
            url: str,
            headers: dict | None = None,
    ) -> httpx.Response:
        headers = headers or self.settings.headers()
        res = httpx.delete(url, headers=headers, timeout=30)
        raise_for_rm_status(res)
        return res


class RoyalMailClient(_RMBaseClient):
    # ORDERS
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
        response = self._do_get(
            url=ORDERS_ENDPOINT,
            headers=self.settings.headers_bearer(),
            params=params
        )
        response_model = GetOrdersResponse.model_validate(response.json())
        pprint(response_model.model_dump(), indent=4, width=120)
        return response_model

    def order_create(self, orders: CreateOrderRequestContainer) -> CreateOrdersResponse:
        res = self._do_post(url=ORDERS_ENDPOINT, data=orders, headers=self.settings.headers_bearer())
        return CreateOrdersResponse.model_validate(res.json())

    def order_cancel(self, order_ident: str | int) -> DeleteOrdersResource:
        ident = str(order_ident)
        url = ORDERS_ENDPOINT + f'/{ident}'
        res = self._do_delete(url=url, headers=self.settings.headers_bearer())
        return DeleteOrdersResource.model_validate(res.json())

    def order_create_return(self, return_request: ReturnsRequest | dict):
        resp = self._do_post(url=RETURNS_ENDPOINT, data=return_request, headers=self.settings.headers_bearer())
        returns_response = ReturnsResponse.model_validate(resp.json())
        return returns_response

    # ADDRESS
    def address_fetch(self, address_id: str) -> AddressRecord:
        resp = self._do_get(url=f'{ADDRESS_BASE_URL}/address/{address_id}')
        return AddressRecord.model_validate(resp.json())

    def address_search(self, address_search_str: str) -> list[AddressSummary]:
        addr_search = AddressFindRequest(address_text=address_search_str)
        resp = self._do_post(url=f'{ADDRESS_BASE_URL}/address', data=addr_search)
        return [AddressSummary.model_validate(_) for _ in resp.json()['addresses']]

    def address_search_dps(self, address_search: AddressFindDPSRequest | dict) -> list[AddressFindDPSResponse]:
        resp = self._do_post(url=f'{ADDRESS_BASE_URL}/address/dps', data=address_search)
        return [AddressFindDPSResponse.model_validate(_) for _ in resp.json()]

    # COLLECTION
    def collection_create(self, data: Collection | dict):
        resp = self._do_post(url=CREATE_URL, data=data)
        return resp

    def collection_slots_fetch(self, dps: str, item_count: int | str) -> GetAvailableSlotsResponse:
        params = {'dps': dps, 'itemCount': item_count}
        resp = self._do_get(url=f'{COLLECTION_HANDLER_BASE}/slots', params=params).json()
        slots = GetAvailableSlotsResponse(**resp)
        return slots

    # DELIVERY OFFICE
    def delivery_office_get(self, postcode: str):
        delivery_office_url = r'https://api.royalmail.net/deliveryOffices'
        params = {'postcode': postcode.replace(' ', '')}
        return self._do_get(url=delivery_office_url, params=params).json()
