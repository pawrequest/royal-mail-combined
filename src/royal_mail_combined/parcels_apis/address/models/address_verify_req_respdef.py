from __future__ import annotations

from pydantic import Field

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import StrictStr2, StrictStr64

from .address_verifydef import AddressVerifyDef


class AddressVerifyReqRespdef(RMBaseModel):
    input: AddressVerifyDef | None = Field(default=None, alias='Input')
    dps: StrictStr2 | None = Field(default=None, alias='DPS')
