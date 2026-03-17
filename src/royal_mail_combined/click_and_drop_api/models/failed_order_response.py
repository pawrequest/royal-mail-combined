from __future__ import annotations
import re  # noqa: F401

from ..models.create_order_error_response import CreateOrderErrorResponse
from ..models.create_order_request import CreateOrderRequest


from royal_mail_combined.core import RMBaseModel


class FailedOrderResponse(RMBaseModel):
    order: CreateOrderRequest | None = None
    errors: list[CreateOrderErrorResponse] | None = None
