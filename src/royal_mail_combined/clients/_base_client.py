import httpx
from loguru import logger

from royal_mail_combined import RMBaseModel
from royal_mail_combined.config import RMSettings

class APIError(Exception):
    def __init__(self, http_code, http_message, more_information):
        super().__init__(f'{http_code}: {http_message} - {more_information}')
        self.http_code = http_code
        self.http_message = http_message
        self.more_information = more_information


def raise_for_rm_status(res):
    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as e:
        logger.error('Royal Mail HTTP Status Error: ' + str(e))
        err = res.json()
        if 'httpCode' in err:
            e = APIError(err['httpCode'], err.get('httpMessage', ''), err.get('moreInformation', ''))
        raise e


class _RMBaseClient(RMBaseModel):
    settings: RMSettings

    def _do_post(
        self,
        *,
        url: str,
        data: dict | None = None,
    ) -> httpx.Response:
        res = httpx.post(url, headers=self.settings.headers(), json=data, timeout=30)
        raise_for_rm_status(res)
        return res

    def _do_get(
        self,
        *,
        url: str,
        params: dict | None = None,
    ) -> httpx.Response:
        res = httpx.get(url, headers=self.settings.headers(), params=params, timeout=30)
        raise_for_rm_status(res)
        return res




