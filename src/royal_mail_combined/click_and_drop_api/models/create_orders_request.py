from __future__ import annotations

from typing import Self

from pydantic import model_validator

from royal_mail_combined.core import RMBaseModel
from ..models.create_order_request import CreateOrderRequest
from ...core.consts_types import RoyalMailServiceCodes


class CreateOrdersRequest(RMBaseModel):
    items: list[CreateOrderRequest]

    @model_validator(mode="after")
    def fix_request(self):
        fixed_orders = []
        for order in self.items:
            if (
                order.postage_details.service_code
                in [
                    RoyalMailServiceCodes.TRACKED_24,
                    RoyalMailServiceCodes.TRACKED_24_RTN,
                ]
                and len(order.packages) > 1
            ):
                for i, package in enumerate(order.packages):
                    fixed_orders.append(
                        order.model_copy(
                            deep=True, update={"packages": [package], "order_reference": f'{order.order_reference}{i:03}'}
                        )
                    )
            else:
                fixed_orders.append(order)
        self.items = fixed_orders
        return self
