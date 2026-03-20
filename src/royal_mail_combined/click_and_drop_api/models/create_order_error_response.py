from __future__ import annotations

import re  # noqa: F401

from pydantic import Field, StrictInt, StrictStr

from royal_mail_combined.click_and_drop_api.models.order_field_response import OrderFieldResponse
from royal_mail_combined.core import RMBaseModel


class CreateOrderErrorResponse(RMBaseModel):
    error_code: StrictInt | None = Field(default=None, alias='errorCode')
    error_message: StrictStr | None = Field(default=None, alias='errorMessage')
    fields: list[OrderFieldResponse] | None = None

    def __str__(self):
        return f'Error in {[str(_) for _ in self.fields]}: {self.error_code} - {self.error_message}'
