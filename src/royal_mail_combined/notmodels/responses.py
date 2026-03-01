from datetime import datetime

from pydantic import Field, StrictInt, StrictStr

from royal_mail_combined import RMBaseModel
from royal_mail_combined.models.click_and_drop import CreateOrderRequest
from royal_mail_combined.models.orders import GetOrderInfoResource


class CreateOrderLabelErrorResponse(RMBaseModel):
    message: StrictStr | None = None


class OrderFieldResponse(RMBaseModel):
    field_name: StrictStr | None = None
    value: StrictStr | None = None


class CreateOrderResponse(RMBaseModel):
    order_identifier: StrictInt = None
    order_reference: StrictStr | None = None
    created_on: datetime = None
    order_date: datetime | None = None
    printed_on: datetime | None = None
    manifested_on: datetime | None = None
    shipped_on: datetime | None = None
    tracking_number: StrictStr | None = None
    label: StrictStr | None = Field(default=None, description='label in format base64 string')
    label_errors: list[CreateOrderLabelErrorResponse] | None = None
    generated_documents: list[StrictStr] | None = None


class CreateOrderErrorResponse(RMBaseModel):
    """
    CreateOrderErrorResponse
    """

    error_code: StrictInt | None = None
    error_message: StrictStr | None = None
    fields: list[OrderFieldResponse] | None = None


class FailedOrderResponse(RMBaseModel):
    order: CreateOrderRequest | None = None
    errors: list[CreateOrderErrorResponse] | None = None


class CreateOrdersResponse(RMBaseModel):
    success_count: StrictInt | None = None
    errors_count: StrictInt | None = None
    created_orders: list[CreateOrderResponse] = Field(default_factory=list)
    failed_orders: list[FailedOrderResponse] = Field(default_factory=list)

    @property
    def created_orders_idents(self) -> list[int]:
        return [_.order_identifier for _ in self.created_orders]

    @property
    def created_orders_idents_str(self) -> str:
        return ','.join(str(_) for _ in self.created_orders_idents)


class GetOrdersResponse(RMBaseModel):
    """
    GetOrdersResponse
    """

    orders: list[GetOrderInfoResource] | None = None
    continuation_token: StrictStr | None = None

    @property
    def order_ident_string(self):
        return ';'.join(str(_.order_identifier) for _ in self.orders)
