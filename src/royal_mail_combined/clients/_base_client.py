import httpx
from pydantic import BaseModel

from royal_mail_combined import RMBaseModel
from royal_mail_combined.clients.exceptions import raise_for_rm_status
from royal_mail_combined.config import RMSettings


class _RMBaseClient(RMBaseModel):
    settings: RMSettings

    def _do_post(
        self,
        *,
        url: str,
        data: dict | None | BaseModel = None,
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
        params: dict | None | BaseModel = None,
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







