import httpx

from royal_mail_combined import RMBaseModel
from royal_mail_combined.config import RMSettings
from royal_mail_combined.endpoints import ADDRESS_FIND
from royal_mail_combined.models.address import AddressFindRequestDef


# from apc_hypaship.config import APCSettings, APCBaseModel
# from apc_hypaship.models.response.label_track import Tracks
# from apc_hypaship.models.response.resp import BookingResponse, ServiceAvailabilityResponse
# from apc_hypaship.models.response.shipment import Label
# from apc_hypaship.models.request.shipment import Shipment

# ResponseMode = Literal['raw'] | Literal['json'] | type


class RMClient(RMBaseModel):
    settings: RMSettings

    def search_address(self, address_search_str: str):
        addr_search = AddressFindRequestDef(address_text=address_search_str).model_dump(
            by_alias=True
        )
        return self._do_post(url=ADDRESS_FIND, data=addr_search)

    def _do_post(
        self,
        *,
        url: str,
        data: dict | None = None,
    ) -> httpx.Response:
        headers = self.settings.headers
        res = httpx.post(url, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        return res

    def _do_get(
        self,
        *,
        url: str,
        params: dict | None = None,
    ) -> httpx.Response:
        headers = self.settings.headers
        res = httpx.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        return res




