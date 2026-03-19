from __future__ import annotations

import re  # noqa: F401

from pydantic import Field, StrictInt

from royal_mail_combined.core import RMBaseModel

from ...converters_no_import import order_idents_str
from ..models.create_order_response import CreateOrderResponse
from ..models.failed_order_response import FailedOrderResponse


class CreateOrdersResponse(RMBaseModel):
    success_count: StrictInt | None = Field(default=None, alias='successCount')
    errors_count: StrictInt | None = Field(default=None, alias='errorsCount')
    created_orders: list[CreateOrderResponse] | None = Field(default=None, alias='createdOrders')
    failed_orders: list[FailedOrderResponse] | None = Field(default=None, alias='failedOrders')

    @property
    def success_idents_str(self) -> str:
        return order_idents_str(self.success_idents)

    @property
    def success_idents(self) -> list:
        return [_.order_identifier for _ in self.created_orders]

    @property
    def failed_idents(self) -> list:
        return [_.order.order_identifier for _ in self.failed_orders]

    @property
    def failed_idents_str(self) -> str:
        return order_idents_str(self.failed_idents)
