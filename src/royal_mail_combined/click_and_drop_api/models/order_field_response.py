from __future__ import annotations

import re  # noqa: F401

from pydantic import StrictStr

from royal_mail_combined.core import RMBaseModel


class OrderFieldResponse(RMBaseModel):
    field_name: StrictStr | None = None
    value: StrictStr | None = None

    def __str__(self):
        return f'Field={self.field_name or "Unknown"}: Value={self.value or "None"}'
