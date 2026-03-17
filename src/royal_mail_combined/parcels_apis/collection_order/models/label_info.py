from __future__ import annotations

import re  # noqa: F401
from datetime import date
from typing import Annotated

from annotated_types import MaxLen
from pydantic import Field, StrictFloat, StrictInt, StrictStr

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import (
    LabelPackageFormat,
    StrictStr13,
    StrictStr20,
    StrictStr21,
    StrictStr40,
    StrictStr50,
)

from ...address.models.address import LabelAddress
from .label_customs_info import LabelCustomsInfo


class LabelInfo(RMBaseModel):
    var_1_d_tracking_number: StrictStr13 | None = Field(alias='1DTrackingNumber')
    var_2_d_unique_identifier: StrictStr21 = Field(alias='2DUniqueIdentifier')
    post_by_date: date = Field(alias='postByDate')
    rm_service: StrictStr50 = Field(alias='RMService')
    price_paid: StrictFloat | StrictInt = Field(description='price paid for the postage', alias='pricePaid')
    reference_number: StrictStr20 | None = None
    reference_text: StrictStr40 | None = None
    weight_in_grams: Annotated[int, Field(strict=True, ge=0)]
    item_format: LabelPackageFormat
    recipient_address: LabelAddress
    sender_address: LabelAddress
    customs_info: LabelCustomsInfo | None = None
    smth: Annotated[StrictStr, MaxLen(5)]
