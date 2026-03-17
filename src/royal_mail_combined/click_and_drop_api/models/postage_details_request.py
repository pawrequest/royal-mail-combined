from __future__ import annotations

import re  # noqa: F401
from datetime import datetime
from typing import Annotated

from pydantic import Field, StrictBool, StrictStr

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import (
    StrictStr2,
    StrictStr10,
    StrictStr35,
    StrictStr50,
    StrictStr90,
    StrictStr150,
)


class PostageDetailsRequest(RMBaseModel):
    send_notifications_to: StrictStr | None = None
    service_code: StrictStr10 | None = None
    carrier_name: StrictStr50 | None = None
    service_register_code: StrictStr2 | None = None
    consequential_loss: Annotated[int, Field(le=10000, strict=True, ge=0)] | None = None
    receive_email_notification: StrictBool | None = None
    receive_sms_notification: StrictBool | None = None
    guaranteed_saturday_delivery: None = None  # Deprecated
    request_signature_upon_delivery: StrictBool | None = None
    is_local_collect: StrictBool | None = None
    safe_place: StrictStr90 | None = Field(default=None, alias='safePlace')
    department: StrictStr150 | None = None
    air_number: StrictStr50 | None = Field(
        default=None,
        description='For B2B orders shipping from Great Britain to Northern Ireland, this field can be used to provide the Recipient UKIMs number.',
        alias='AIRNumber',
    )
    ioss_number: StrictStr50 | None = Field(default=None, alias='IOSSNumber')
    requires_export_license: StrictBool | None = None
    commercial_invoice_number: StrictStr35 | None = None
    commercial_invoice_date: datetime | None = None
    recipient_eori_number: StrictStr | None = None
