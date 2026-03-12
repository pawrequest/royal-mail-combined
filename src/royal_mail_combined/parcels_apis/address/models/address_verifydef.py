from __future__ import annotations
import re  # noqa: F401

from pydantic import Field
from typing import Annotated

from royal_mail_combined import RMBaseModel


class AddressVerifyDef(RMBaseModel):
    """
    Summary of the matching address
    """

    address_line1: Annotated[str, Field(min_length=1, strict=True, max_length=64)]
    address_line2: Annotated[str, Field(strict=True, max_length=64)] | None = None
    address_line3: Annotated[str, Field(strict=True, max_length=64)] | None = None
    post_town: Annotated[str, Field(min_length=1, strict=True, max_length=64)]
    county: Annotated[str, Field(strict=True, max_length=64)] | None = Field(default=None, alias='County')
    postcode: Annotated[str, Field(min_length=1, strict=True, max_length=10)]
