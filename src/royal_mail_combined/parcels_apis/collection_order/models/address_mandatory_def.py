from __future__ import annotations

from pydantic import Field

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import StrictStr10, StrictStr64


class AddressMandatoryDef(RMBaseModel):
    address_line1: StrictStr64
    address_line2: StrictStr64 | None = None
    address_line3: StrictStr64 | None = None
    post_town: StrictStr64
    postcode: StrictStr10
    dps: StrictStr10 = Field(description="Delivery Point Suffix", alias="DPS")
    county: StrictStr64 | None = Field(default=None, alias="County")
