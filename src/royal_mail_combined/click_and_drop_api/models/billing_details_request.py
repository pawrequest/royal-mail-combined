from __future__ import annotations

import re  # noqa: F401
from typing import Annotated

from pydantic import Field

from royal_mail_combined.click_and_drop_api.models import AddressRequest
from royal_mail_combined.core import RMBaseModel


class BillingDetailsRequest(RMBaseModel):
    """
    <b>Billing</b> along with <b>billing.address</b> objects are required in specific case when 'Use shipping address for billing address' setting is set to 'false' and 'Recipient.AddressBookReference' is provided.
    """

    address: AddressRequest | None = None
    phone_number: Annotated[str, Field(strict=True, max_length=25)] | None = Field(default=None, alias='phoneNumber')
    email_address: Annotated[str, Field(strict=True, max_length=254)] | None = Field(default=None, alias='emailAddress')
