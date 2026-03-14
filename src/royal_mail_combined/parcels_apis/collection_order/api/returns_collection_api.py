from datetime import date
from typing import Annotated, Any

from pydantic import Field, StrictFloat, StrictInt, StrictStr, validate_call

from royal_mail_combined.core.api_response import ApiResponse
from royal_mail_combined.core.consts_types import X_RMG_DATETIME
from royal_mail_combined.core.core_api_client import RequestSerialized
from royal_mail_combined.core.rest import RESTResponseType
from royal_mail_combined.parcels_apis.collection_order.models import (
    DraftCollectionLabelRequest,
    DraftCollectionLabelResult,
)


class ReturnsCollectionApi:
    def __init__(self, api_client) -> None:
        self.api_client = api_client

    @validate_call
    def post_draft_collection_item(
        self,
        label_info: Annotated[DraftCollectionLabelRequest, Field(description="Provide the label information")],
        x_rmg_date_time: X_RMG_DATETIME,
        x_rmg_language: Annotated[StrictStr | None, Field(description="Optional default english")] = None,
        accept: Annotated[StrictStr | None, Field(description="Pass though; used for markdown")] = None,
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> DraftCollectionLabelResult:
        """Create a draft collection label item


        :param x_rmg_date_time: This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00 (required)
        :type x_rmg_date_time: date
        :param label_info: Provide the label information (required)
        :type label_info: DraftCollectionLabelRequest
        :param x_rmg_language: Optional default english
        :type x_rmg_language: str
        :param accept: Pass though; used for markdown
        :type accept: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._post_draft_collection_item_serialize(
            x_rmg_date_time=x_rmg_date_time,
            label_info=label_info,
            x_rmg_language=x_rmg_language,
            accept=accept,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "DraftCollectionLabelResult",
            "400": "Model400",
            "401": "Model401",
            "404": "Model404",
            "405": "Model405",
            "500": "Model500",
            "503": "Model503",
        }
        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    def post_draft_collection_item_with_http_info(
        self,
        x_rmg_date_time: Annotated[
            date,
            Field(
                description="This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00"
            ),
        ],
        label_info: Annotated[DraftCollectionLabelRequest, Field(description="Provide the label information")],
        x_rmg_language: Annotated[StrictStr | None, Field(description="Optional default english")] = None,
        accept: Annotated[StrictStr | None, Field(description="Pass though; used for markdown")] = None,
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[DraftCollectionLabelResult]:
        """Create a draft collection label item


        :param x_rmg_date_time: This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00 (required)
        :type x_rmg_date_time: date
        :param label_info: Provide the label information (required)
        :type label_info: DraftCollectionLabelRequest
        :param x_rmg_language: Optional default english
        :type x_rmg_language: str
        :param accept: Pass though; used for markdown
        :type accept: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._post_draft_collection_item_serialize(
            x_rmg_date_time=x_rmg_date_time,
            label_info=label_info,
            x_rmg_language=x_rmg_language,
            accept=accept,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "DraftCollectionLabelResult",
            "400": "Model400",
            "401": "Model401",
            "404": "Model404",
            "405": "Model405",
            "500": "Model500",
            "503": "Model503",
        }
        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    def post_draft_collection_item_without_preload_content(
        self,
        x_rmg_date_time: Annotated[
            date,
            Field(
                description="This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00"
            ),
        ],
        label_info: Annotated[DraftCollectionLabelRequest, Field(description="Provide the label information")],
        x_rmg_language: Annotated[StrictStr | None, Field(description="Optional default english")] = None,
        accept: Annotated[StrictStr | None, Field(description="Pass though; used for markdown")] = None,
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Create a draft collection label item


        :param x_rmg_date_time: This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00 (required)
        :type x_rmg_date_time: date
        :param label_info: Provide the label information (required)
        :type label_info: DraftCollectionLabelRequest
        :param x_rmg_language: Optional default english
        :type x_rmg_language: str
        :param accept: Pass though; used for markdown
        :type accept: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._post_draft_collection_item_serialize(
            x_rmg_date_time=x_rmg_date_time,
            label_info=label_info,
            x_rmg_language=x_rmg_language,
            accept=accept,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "DraftCollectionLabelResult",
            "400": "Model400",
            "401": "Model401",
            "404": "Model404",
            "405": "Model405",
            "500": "Model500",
            "503": "Model503",
        }
        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        return response_data.response

    def _post_draft_collection_item_serialize(
        self,
        x_rmg_date_time,
        label_info,
        x_rmg_language,
        accept,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: dict[str, str] = {}

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[str, str | bytes | list[str] | list[bytes] | list[tuple[str, bytes]]] = {}
        _body_params: bytes | None = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if x_rmg_language is not None:
            _header_params["X-RMG-Language"] = x_rmg_language
        if x_rmg_date_time is not None:
            _header_params["X-RMG-Date-Time"] = x_rmg_date_time
        if accept is not None:
            _header_params["Accept"] = accept
        # process the form parameters
        # process the body parameter
        if label_info is not None:
            _body_params = label_info

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params["Content-Type"] = _content_type
        else:
            _default_content_type = self.api_client.select_header_content_type(["application/json"])
            if _default_content_type is not None:
                _header_params["Content-Type"] = _default_content_type

        # authentication setting
        _auth_settings: list[str] = ["Client-Id", "Client-Secret"]

        return self.api_client.param_serialize(
            method="POST",
            resource_path="/collectionOrder/draftLabel",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )
