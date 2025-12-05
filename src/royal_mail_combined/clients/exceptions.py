import json
import pprint
from dataclasses import dataclass

import httpx
from httpx import Request, Response
from loguru import logger


@dataclass
class RMError:
    cause: str
    code: str
    description: str
    resolution: str


class RMStatusError(httpx.HTTPStatusError):
    http_code: int
    http_message: str
    more_information: str
    errors: list[RMError]

    def __init__(self, request: Request, response: Response | None = None):
        err_json = response.json()
        self.http_code = err_json.get('httpCode', response.status_code)
        self.http_message = err_json.get('httpMessage', '')
        self.more_information = err_json.get('moreInformation', '')
        errors_json = err_json.get('errors', [])
        self.errors = [RMError(**_) for _ in errors_json]

        more_msg = f' - "{self.more_information}"' if self.more_information else ''
        errors_msg = f' - {'\n'.join([str(_) for _ in self.errors])}' if self.errors else ''
        msg = f'RoyalMail Http Status error for {request.url}: {self.http_code}: {self.http_message}{more_msg}{errors_msg}'
        super().__init__(msg, request=request, response=response)


def raise_for_rm_status(response: Response):
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as httpx_error:
        rm_error = RMStatusError(request=response.request, response=response)

        if response.request.content:
            request_content = json.loads(response.request.content.decode())
            failed_req = '\n Failed Request: ' + pprint.pformat(request_content, indent=4)
        else:
            failed_req = ''

        msg = rm_error.args[0] + failed_req
        logger.error(msg)
        raise rm_error from httpx_error

