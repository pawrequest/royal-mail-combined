from __future__ import annotations

import re  # noqa: F401
from typing import Annotated

from pydantic import Field

from royal_mail_combined.core import RMBaseModel


class SenderDetailsRequest(RMBaseModel):
    trading_name: Annotated[str, Field(strict=True, max_length=250)] | None = Field(default=None, alias='tradingName')
    phone_number: Annotated[str, Field(strict=True, max_length=25)] | None = Field(default=None, alias='phoneNumber')
    email_address: Annotated[str, Field(strict=True, max_length=254)] | None = Field(default=None, alias='emailAddress')
