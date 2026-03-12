from __future__ import annotations

import re  # noqa: F401

from pydantic import Field
from typing import Annotated


from royal_mail_combined import RMBaseModel


class AddressFindRequestDef(RMBaseModel):
    address_text: Annotated[str, Field(min_length=12, strict=True, max_length=200)]
