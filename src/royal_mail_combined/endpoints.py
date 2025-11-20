# from dataclasses import dataclass, field
# from datetime import datetime
# from typing import Literal
#
# HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]
#
#
# #  example date 2016-10-20T10:04:00+01:00
#
#
# def rm_format_date(d: datetime):
#     return d.strftime("%Y-%m-%dT%H:%M:%S%z")
#
#
# @dataclass
# class _Endpoint:
#     base_url: str
#     method: HttpMethod
#     body: dict[str, type] = field(default_factory=dict)
#     path: str = ""
#     query_params: dict[str, type] = field(default_factory=dict)
#     required_headers: dict[str, type] = field(default_factory=dict)
#     optional_headers: dict[str, type] = field(default_factory=dict)
#
#
# #
# # @dataclass
# # class Endpoint:
# #     url: str
# #     method: HttpMethod
# #     required_params: dict[str, type] = field(default_factory=dict)
# #     optional_params: dict[str, type] = field(default_factory=dict)
# #     required_headers: dict[str, type] = field(default_factory=dict)
# #     optional_headers: dict[str, type] = field(default_factory=dict)
# #
# #
# # AddressFind = Endpoint(
# #     url=f"{ADDRESS_BASE}/address",
# #     method="POST",
# #     required_headers={
# #         "X-RMG-Date-Time": str,
# #     },
# #     optional_headers={
# #         "X-RMG-Language": str,
# #     },
# #     required_params={
# #         "addressFindRequest": dict,
# #     },
# # )
