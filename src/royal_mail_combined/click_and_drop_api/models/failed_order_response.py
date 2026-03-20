from __future__ import annotations

import re  # noqa: F401

from royal_mail_combined.core import RMBaseModel

from ..models.create_order_error_response import CreateOrderErrorResponse
from ..models.create_order_request import CreateOrderRequest


class FailedOrderResponse(RMBaseModel):
    order: CreateOrderRequest | None = None
    errors: list[CreateOrderErrorResponse] | None = None

    def __str__(self):
        order_ident = self.order.order_reference if self.order else 'Unknown'
        error_messages = ', '.join(str(e) for e in self.errors) if self.errors else 'No errors'
        return f'Order reference "{order_ident}" failed, errors=[{error_messages}])'
