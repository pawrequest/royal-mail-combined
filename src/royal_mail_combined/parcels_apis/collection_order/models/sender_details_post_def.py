from __future__ import annotations

import re  # noqa: F401
from typing import Annotated

from pydantic import Field

from royal_mail_combined.core import RMBaseModel


class SenderDetailsPostDef(RMBaseModel):
    sender_name: Annotated[str, Field(min_length=1, strict=True, max_length=100)]
    sender_email: Annotated[str, Field(min_length=1, strict=True, max_length=50)]
