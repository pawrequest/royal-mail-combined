from __future__ import annotations

from typing import Annotated

from pydantic import Field

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import StrictStr2, StrictStr3, StrictStr10, StrictStr50, StrictStr64


class AddressDefault(RMBaseModel):
    address_line1: StrictStr64 | None = None
    address_line2: StrictStr64 | None = None
    address_line3: StrictStr64 | None = None
    post_town: StrictStr64 | None = None
    postcode: StrictStr10 | None = None
    dps: StrictStr10 | None = Field(default=None, alias='DPS', description='Delivery Point Suffix With Postcode')
    county: StrictStr64 | None = Field(default=None, alias='County')  # Pascal
    name: StrictStr50 | None = None
    company_name: StrictStr50 | None = None
    # country_code: StrictStr3 | None = 'GBR'


class AddressBasic(AddressDefault):
    address_line1: StrictStr64  # required
    postcode: StrictStr10  # required


class AddressVerifable(AddressBasic):
    post_town: StrictStr64  # required


class AddressDps(AddressVerifable):
    dps: StrictStr10 = Field(description='Delivery Point Suffix', alias='DPS')  # required


class AddressVerifiableList(RMBaseModel):
    addresses: list[AddressVerifable] | None = Field(default=None, alias='Addresses', min_length=1, max_length=100)


class AddressFindRequest(RMBaseModel):
    address_text: Annotated[str, Field(min_length=12, strict=True, max_length=200)]


class AddressVerified(RMBaseModel):
    input: AddressVerifable | None = Field(default=None, alias='Input')
    dps: StrictStr2 | None = Field(default=None, alias='DPS')


class LabelAddress(AddressVerifable):
    # overrides
    county: StrictStr64 | None = Field(None, alias='county')  # camel
    dps: StrictStr2 = Field(default='9Z', alias='DPS', description=' Delivery Point Suffix Without postcode')
