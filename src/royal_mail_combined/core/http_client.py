import httpx
from pydantic import BaseModel

from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.exceptions import raise_for_rm_status


class RMBaseClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        self.settings = settings

    def do_post(
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

    def do_get(
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

    def do_delete(
            self,
            *,
            url: str,
            headers: dict | None = None,
    ) -> httpx.Response:
        headers = headers or self.settings.headers()
        res = httpx.delete(url, headers=headers, timeout=30)
        raise_for_rm_status(res)
        return res

    def do_put(self, *, url: str, data: dict | BaseModel | None = None, headers: dict | None = None) -> httpx.Response:
        headers = headers or self.settings.headers()
        if isinstance(data, BaseModel):
            data = data.model_dump(mode='json', by_alias=True)
        res = httpx.put(url, headers=headers, json=data, timeout=30)
        raise_for_rm_status(res)
        return res
