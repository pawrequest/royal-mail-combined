from royal_mail_combined.clients._base_client import _RMBaseClient
from royal_mail_combined.models.address import (
    AddressFindRequest,
    AddressRecord,
    AddressSummary,
)

ADDRESS_BASE_URL = r'https://api.royalmail.net/addressfind/v1'


class AddressClient(_RMBaseClient):
    def search(self, address_search_str: str) -> list[AddressSummary]:
        addr_search = AddressFindRequest(address_text=address_search_str).model_dump(by_alias=True)
        resp = self._do_post(url=f'{ADDRESS_BASE_URL}/address', data=addr_search).json()
        summaries = [AddressSummary.model_validate(_) for _ in resp['addresses']]
        return summaries

    def search_dps(self, address_search: dict) -> list[AddressSummary]:
        # addr_search = AddressFindRequest(address_text=address_search_str).model_dump(by_alias=True)
        resp = self._do_post(url=f'{ADDRESS_BASE_URL}/address/dps', data=address_search).json()
        summaries = [AddressSummary.model_validate(_) for _ in resp['addresses']]
        return summaries

    def get(self, address_id: str) -> AddressRecord:
        resp = self._do_get(url=f'{ADDRESS_BASE_URL}/address/{address_id}').json()
        address_record = AddressRecord.model_validate(resp)
        return address_record
