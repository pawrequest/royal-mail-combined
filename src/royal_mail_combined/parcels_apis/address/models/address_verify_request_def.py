from __future__ import annotations

from pydantic import Field

from royal_mail_combined.core import RMBaseModel

from .address_verifydef import AddressVerifyDef


class AddressVerifyRequestDef(RMBaseModel):
    addresses: list[AddressVerifyDef] | None = Field(default=None, alias="Addresses", min_length=1, max_length=100)
