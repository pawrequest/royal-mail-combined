from __future__ import annotations

import re  # noqa: F401

from pydantic import Field, StrictStr

from royal_mail_combined.core import RMBaseModel


class CollectionOrderCreateResponse(RMBaseModel):
    collection_order_id: StrictStr
    status: StrictStr = Field(alias="Status")
