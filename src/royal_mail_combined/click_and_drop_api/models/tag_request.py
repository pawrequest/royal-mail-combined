from __future__ import annotations
import re  # noqa: F401

from pydantic import Field
from typing import Annotated

from royal_mail_combined.core import RMBaseModel


class TagRequest(RMBaseModel):
    key: Annotated[str, Field(strict=True, max_length=100)] | None = None
    value: Annotated[str, Field(strict=True, max_length=100)] | None = None
