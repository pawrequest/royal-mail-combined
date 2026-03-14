from __future__ import annotations

import re  # noqa: F401
from datetime import date
from typing import Annotated

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr

from royal_mail_combined.core import RMBaseModel

from ...address.models.address import LabelAddress
from .label_customs_info import LabelCustomsInfo


class DraftCollectionLabelRequest(RMBaseModel):
    var_1_d_tracking_number: str = Field(min_length=1, strict=True, max_length=13, alias="1DTrackingNumber")
    var_2_d_unique_identifier: str = Field(min_length=1, strict=True, max_length=21, alias="2DUniqueIdentifier")
    post_by_date: date | None = None
    rm_service: str | None = Field(default=None, alias="RMService", strict=True, max_length=50)
    price_paid: StrictFloat | StrictInt | None = Field(default=None, alias="pricePaid")
    reference_number: Annotated[str, Field(strict=True, max_length=20)] | None = None
    display_reference_as_barcode: StrictBool | None = None
    reference_text: Annotated[str, Field(strict=True, max_length=40)] | None = None
    weight_in_grams: StrictInt | None = Field(default=None, alias="weightInGrams")
    item_format: StrictStr | None = Field(default=None, alias="itemFormat")
    recipient_address: LabelAddress
    sender_address: LabelAddress | None = None
    customs_info: LabelCustomsInfo | None = None
