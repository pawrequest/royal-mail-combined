import json
import pprint
from dataclasses import dataclass
from json import JSONDecodeError

import httpx
from httpx import Request, Response
from loguru import logger


@dataclass
class RMError:
    cause: str
    code: str
    description: str
    resolution: str


# class RMStatusError(httpx.HTTPStatusError):
#     http_code: int
#     http_message: str
#     more_information: str
#     errors: list[RMError]
#
#     def __init__(self, request: Request, response: Response | None = None):
#         try:
#             err_json = response.json()
#         except JSONDecodeError as e:
#             msg = f'RoyalMail Http Status error for {request.url}: Unable to decode error response JSON: {e}'
#             super().__init__(msg, request=request, response=response)
#             return
#
#         self.http_code = err_json.get('httpCode', response.status_code)
#         self.http_message = err_json.get('httpMessage', '')
#         self.more_information = err_json.get('moreInformation', '')
#         errors_json = err_json.get('errors', [])
#         self.errors = [RMError(**_) for _ in errors_json]
#
#         more_msg = f' - "{self.more_information}"' if self.more_information else ''
#         errors_msg = f' - {'\n'.join([str(_) for _ in self.errors])}' if self.errors else ''
#         msg = f'RoyalMail Http Status error for {request.url}: {self.http_code}: {self.http_message}{more_msg}{errors_msg}'
#         super().__init__(msg, request=request, response=response)


class RMStatusError2(httpx.HTTPStatusError):
    http_code: int | None = None
    http_message: str = ''
    more_information: str = ''
    errors: list[RMError] = None
    a_msg: str = ''

    def __init__(self, http_error: httpx.HTTPStatusError):
        request = http_error.request
        response = http_error.response
        try:
            err_json = response.json()
        except JSONDecodeError as e:
            super().__init__(str(http_error), request=request, response=response)
            self.errors = []
            return

        self.http_code = err_json.get('httpCode', response.status_code)
        self.http_message = err_json.get('httpMessage', '')
        self.more_information = err_json.get('moreInformation', '')
        self.a_msg = err_json.get('message', '')
        errors_json = err_json.get('errors', [])
        self.errors = [RMError(**_) for _ in errors_json]

        infos = [self.http_code, self.http_message, self.more_information, self.a_msg]
        infos_str = ' | '.join([str(i) for i in infos if i])
        msg = f'RoyalMail Http Status error for {request.url}: {infos_str}'
        super().__init__(msg, request=request, response=response)
        ...


def raise_for_rm_status(response: Response):
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as httpx_error:
        rm_error = RMStatusError2(http_error=httpx_error)
        # rm_error = RMStatusError(request=response.request, response=response)

        if response.request.content:
            request_content = json.loads(response.request.content.decode())
            failed_req = '\n Failed Request: ' + pprint.pformat(request_content, indent=4)
        else:
            failed_req = ''

        msg = str(rm_error) + failed_req
        logger.error(msg)
        raise rm_error from httpx_error

