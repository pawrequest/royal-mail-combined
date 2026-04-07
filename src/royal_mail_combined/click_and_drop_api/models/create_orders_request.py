from __future__ import annotations

from loguru import logger
from pydantic import model_validator

from royal_mail_combined.click_and_drop_api.models.create_order_request import CreateOrderRequest
from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import RoyalMailServiceCodes


class CreateOrdersRequest(RMBaseModel):
    items: list[CreateOrderRequest]

    @model_validator(mode='after')
    def tracked24_one_package_per_order(self):
        if len(self.items) == 1 and len(self.items[0].packages) == 1:
            return self
        fixed_orders = []
        for order in self.items:
            if (
                order.postage_details.service_code
                in [
                    RoyalMailServiceCodes.TRACKED_24,
                    RoyalMailServiceCodes.TRACKED_24_RTN,
                    RoyalMailServiceCodes.SPECIAL_1PM,
                ]
                and len(order.packages) > 1
            ):
                for i, package in enumerate(order.packages, start=1):
                    new_ref = order.order_reference[0:34] + f' {i}/{len(order.packages)}'
                    logger.info(
                        f'Order {order.order_reference or order.recipient.address.postcode} has service code '
                        f'{order.postage_details.service_code} and more than 1 package - '
                        f'Splitting into separate orders for each package.'
                    )
                    fixed_orders.append(
                        order.model_copy(
                            deep=True,
                            update={'packages': [package], 'order_reference': new_ref},
                        )
                    )
            else:
                fixed_orders.append(order)
        self.items = fixed_orders
        return self
