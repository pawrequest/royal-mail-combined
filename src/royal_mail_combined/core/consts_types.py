from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Annotated

from annotated_types import Ge, Le, MultipleOf
from pydantic import Field, StrictFloat, StrictInt, StringConstraints

# Types
StrictStr2 = Annotated[str, StringConstraints(max_length=2, strict=True)]
StrictStr3 = Annotated[str, StringConstraints(max_length=3, strict=True)]
StrictStr5 = Annotated[str, StringConstraints(max_length=5, strict=True)]
StrictStr10 = Annotated[str, StringConstraints(max_length=10, strict=True)]
StrictStr13 = Annotated[str, StringConstraints(max_length=13, strict=True)]
StrictStr20 = Annotated[str, StringConstraints(max_length=20, strict=True)]
StrictStr21 = Annotated[str, StringConstraints(max_length=21, strict=True)]
StrictStr35 = Annotated[str, StringConstraints(max_length=35, strict=True)]
StrictStr40 = Annotated[str, StringConstraints(max_length=40, strict=True)]
StrictStr50 = Annotated[str, StringConstraints(max_length=50, strict=True)]
StrictStr64 = Annotated[str, StringConstraints(max_length=64, strict=True)]
StrictStr90 = Annotated[str, StringConstraints(max_length=90, strict=True)]
StrictStr100 = Annotated[str, StringConstraints(max_length=100, strict=True)]
StrictStr150 = Annotated[str, StringConstraints(max_length=150, strict=True)]
StrictStr210 = Annotated[str, StringConstraints(max_length=210, strict=True)]

StrictNonNegativeDecimalFloat = Annotated[StrictFloat, Ge(0), Le(999999), MultipleOf(0.01)]
StrictNonNegativeInt = Annotated[StrictInt, Ge(0), Le(999999)]
StrictNonNegativeNumber = StrictNonNegativeDecimalFloat | StrictNonNegativeInt


DatetimeNowIsoSeconds = Annotated[date, Field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))]


# Enums
class ItemStatus(StrEnum):
    AWAITING_COLLECTION = 'AwaitingCollection'
    COLLECTED = 'Collected'
    NOT_COLLECTED = 'NotCollected'
    PROCESSING = 'Processing'
    ATTEMPTED = 'Attempted'


class CollectionStatus(StrEnum):
    CREATED = 'Created'
    PENDING = 'Pending'
    COLLECTIONORDERPLACED = 'CollectionOrderPlaced'
    COLLECTED = 'Collected'
    CANCELLED = 'Cancelled'
    PROCESSING = 'Processing'
    NOTCOLLECTED = 'NotCollected'
    ATTEMPTED = 'Attempted'


class SendNotifcationsTo(StrEnum):
    SENDER = 'sender'
    RECIPIENT = 'recipient'
    BILLING = 'billing'


class LabelPackageFormat(StrEnum):
    LETTER = 'Letter'
    LARGE_LETTER = 'LargeLetter'
    SMALL_PARCEL = 'SmallParcel'
    MEDIUM_PARCEL = 'MediumParcel'


class PackageFormat(StrEnum):
    SMALL_PARCEL = 'smallParcel'
    MEDIUM_PARCEL = 'mediumParcel'
    PARCEL = 'parcel'
    LETTER = 'letter'
    LARGE_LETTER = 'largeLetter'
    DOCUMENTS = 'documents'
    UNDEFINED = 'undefined'


class ResponseMessages(StrEnum):
    COLLECTION_CREATED = 'Order created successfully'
    COLLECTION_CANCELLED = 'Order cancelled successfully'


class RoyalMailServiceCodes(StrEnum):
    EXPRESS_24 = 'NDA'
    TRACKED_24 = 'TPN24'  # no signature.
    SPECIAL_1PM = 'SD1'  # Special Delivery Guaranteed by 1pm - £750 (01)
    EXPRESS_AM = 'FEE'  # maybe not real?
    EXPRESS_10 = 'TE1'  # maybe not real?
    TRACKED_24_RTN = 'TSN'


class RoyalMailInboundServiceCodes(StrEnum):
    TRACKED_24_RTN = 'TSN'


class ReturnsServiceNames(StrEnum):
    TRACKED_24 = 'Tracked Returns 24 (T24) Enhanced'


RMTracked24OneBoxOnly = [
    RoyalMailServiceCodes.TRACKED_24,
    RoyalMailServiceCodes.TRACKED_24_RTN,
    RoyalMailServiceCodes.SPECIAL_1PM,
]
