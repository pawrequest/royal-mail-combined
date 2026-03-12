from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Annotated

from pydantic import Field


class SendNotifcationsTo(StrEnum):
    SENDER = 'sender'
    RECIPIENT = 'recipient'
    BILLING = 'billing'


X_RMG_DATETIME = Annotated[
    date,
    Field(
        description='This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00',
        # default_factory=datetime.now().isoformat(timespec='seconds').__str__,
        default_factory=lambda: datetime.now().isoformat(timespec='seconds'),
    ),
]


class PackageFormat(StrEnum):
    SMALL_PARCEL = 'smallParcel'
    MEDIUM_PARCEL = 'mediumParcel'
    PARCEL = 'parcel'
    LETTER = 'letter'
    LARGE_LETTER = 'largeLetter'
    DOCUMENTS = 'documents'
    UNDEFINED = 'undefined'
