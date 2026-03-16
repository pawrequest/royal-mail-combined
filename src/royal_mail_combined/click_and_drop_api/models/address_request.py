from __future__ import annotations

import re  # noqa: F401


from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import StrictStr100, StrictStr20, StrictStr210, StrictStr3


class AddressRequest(RMBaseModel):
    full_name: StrictStr210 | None = None
    company_name: StrictStr100 | None = None
    address_line1: StrictStr100
    address_line2: StrictStr100 | None = None
    address_line3: StrictStr100 | None = None
    city: StrictStr100
    county: StrictStr100 | None = None
    postcode: StrictStr20 | None = None
    country_code: StrictStr3 = "GB"
