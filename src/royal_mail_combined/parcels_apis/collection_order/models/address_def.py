from __future__ import annotations

import re  # noqa: F401

from pydantic import Field

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import StrictStr10, StrictStr64


class AddressDef(RMBaseModel):
    address_line1: StrictStr64 | None = None
    address_line2: StrictStr64 | None = None
    address_line3: StrictStr64 | None = None
    post_town: StrictStr64 | None = None
    postcode: StrictStr10 | None = None
    dps: StrictStr10 | None = Field(alias="DPS", description="Delivery Point Suffix")
    county: StrictStr64 | None = Field(alias="County")
