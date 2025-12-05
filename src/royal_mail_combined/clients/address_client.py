from royal_mail_combined.clients._base_client import _RMBaseClient
from royal_mail_combined.address.address import (
    AddressFindDPSRequest,
    AddressFindDPSResponse,
    AddressFindRequest,
    AddressRecord,
    AddressSummary,
)

ADDRESS_BASE_URL = r'https://api.royalmail.net/addressfind/v1'


class AddressClient(_RMBaseClient):
    def search(self, address_search_str: str) -> list[AddressSummary]:
        addr_search = AddressFindRequest(address_text=address_search_str)
        resp_json = self._do_post(url=f'{ADDRESS_BASE_URL}/address', data=addr_search).json()
        return [AddressSummary.model_validate(_) for _ in resp_json['addresses']]
        # resp = AddressSearchResponse.model_validate(resp_json)

    def search_dps(self, address_search: AddressFindDPSRequest | dict) -> list[AddressFindDPSResponse]:
        resp = self._do_post(url=f'{ADDRESS_BASE_URL}/address/dps', data=address_search).json()
        return [AddressFindDPSResponse.model_validate(_) for _ in resp]

    def get(self, address_id: str) -> AddressRecord:
        resp = self._do_get(url=f'{ADDRESS_BASE_URL}/address/{address_id}').json()
        return AddressRecord.model_validate(resp)
