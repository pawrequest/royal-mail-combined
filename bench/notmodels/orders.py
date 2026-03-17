from datetime import datetime

from pydantic import StrictInt, StrictStr

from royal_mail_combined import RMBaseModel


class GetOrderInfoResource(RMBaseModel):
    """
    GetOrderInfoResource
    """

    order_identifier: StrictInt
    order_reference: StrictStr | None = None
    created_on: datetime
    order_date: datetime | None = None
    printed_on: datetime | None = None
    manifested_on: datetime | None = None
    shipped_on: datetime | None = None
    tracking_number: StrictStr | None = None


class DeletedOrderInfo(RMBaseModel):
    order_identifier: StrictInt | None = None
    order_reference: StrictStr | None = None
    order_info: StrictStr | None = None


class OrderErrorInfo(RMBaseModel):
    """
    OrderErrorInfo
    """

    order_identifier: StrictInt | None = None
    order_reference: StrictStr | None = None
    code: StrictStr | None = None
    message: StrictStr | None = None


class DeleteOrdersResource(RMBaseModel):
    deleted_orders: list[DeletedOrderInfo] | None = None
    errors: list[OrderErrorInfo] | None = None

    @property
    def idents(self) -> list[int]:
        return [_.order_identifier for _ in self.deleted_orders]

    @property
    def idents_str(self) -> str:
        return ','.join(str(_) for _ in self.idents)
