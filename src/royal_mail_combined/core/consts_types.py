from __future__ import annotations

from datetime import date, datetime
from enum import Enum, StrEnum
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


X_RMG_DATETIME = Annotated[
    date,
    Field(
        description="This should be populated with the date time in ISO 8601 subset format below when the message was generated. Eg. 2016-10-20T10:04:00+01:00",
        default_factory=lambda: datetime.now().isoformat(timespec="seconds"),
    ),
]


# Enums
class ItemStatus(StrEnum):
    AWAITING_COLLECTION = "AwaitingCollection"
    COLLECTED = "Collected"
    NOT_COLLECTED = "NotCollected"
    PROCESSING = "Processing"
    ATTEMPTED = "Attempted"


class CollectionStatus(str, Enum):
    CREATED = "Created"
    PENDING = "Pending"
    COLLECTIONORDERPLACED = "CollectionOrderPlaced"
    COLLECTED = "Collected"
    CANCELLED = "Cancelled"
    PROCESSING = "Processing"
    NOTCOLLECTED = "NotCollected"
    ATTEMPTED = "Attempted"


class SendNotifcationsTo(StrEnum):
    SENDER = "sender"
    RECIPIENT = "recipient"
    BILLING = "billing"


class LabelPackageFormat(StrEnum):
    LETTER = "letter"
    LARGE_LETTER = "largeLetter"
    SMALL_PARCEL = "smallParcel"
    MEDIUM_PARCEL = "mediumParcel"


class PackageFormat(StrEnum):
    SMALL_PARCEL = "smallParcel"
    MEDIUM_PARCEL = "mediumParcel"
    PARCEL = "parcel"
    LETTER = "letter"
    LARGE_LETTER = "largeLetter"
    DOCUMENTS = "documents"
    UNDEFINED = "undefined"


class ResponseMessages(StrEnum):
    COLLECTION_CREATED = "Order created successfully"
    COLLECTION_CANCELLED = "Order cancelled successfully"


class RoyalMailServiceCodes(StrEnum):
    TRACKED_24 = "TPN24"  # no signature.
    TRACKED_24_RTN = "TSN"  # no signature.
    EXPRESS_24 = "NDA"
    EXPRESS_24_RTN = "RT0"


class ReturnsServiceNames(StrEnum):
    TRACKED_24 = "Tracked Returns 24 (T24) Enhanced"


# class RoyalMailServiceCodeClickDrop(StrEnum):
#     TRACKED_24 = 'TOLP24'  # no signature.
#     TRACKED_24_SIGNED = 'TOLP24SF'
#     SPECIAL_PRE_12 = 'SD1OLP'  # £750 comp... use 'SD2OLP' for 1,000 or 'SD3OLP' for 2,500
#     EXPRESS_24 = 'PFE24'
#     EXPRESS_24_PRE_10 = 'PFE10'
#     EXPRESS_24_RETURN = 'RT0'
#
#
# class RoyalMailServiceCode(StrEnum):
#     EXPRESS_24 = 'NDA'
#     EXPRESS_24_RETURN = 'RT0'
#     FIRST_CLASS_SIGNED = 'BPR1'
#     EXPRESS_AM = 'FEE'
#     EXPRESS_10 = 'TE1'
#     SPECIAL_1PM = 'SD1'
#     SPECIAL_9AM = 'SD4'
#
#
# class RoyalMailServiceCodeFull(StrEnum):
#     InternationalEconomy = 'IEOLP'
#     InternationalSigned = 'ISIOLP'
#     InternationalSignedDuplicate = 'ISIOLP'
#     InternationalStandard = 'ISOLP'
#     InternationalTrackedHeavier = 'ITHCOLP'
#     InternationalTrackedHeavierDuplicate = 'ITHCOLP'
#     InternationalTrackedSignedHeavier = 'ITHOLPSF'
#     InternationalTrackedSignedHeavierDuplicate = 'ITHOLPSF'
#     InternationalTracked = 'ITROLP'
#     InternationalTrackedDuplicate = 'ITROLP'
#     InternationalTrackedSigned = 'ITSOLP'
#     InternationalTrackedSignedDuplicate = 'ITSOLP'
#     RoyalMail1stClass = 'OLP1'
#     RoyalMailSignedFor1stClass = 'OLP1SF'
#     RoyalMail2ndClass = 'OLP2'
#     RoyalMailSignedFor2ndClass = 'OLP2SF'
#     express10 = 'PFE10'
#     express10Comp1 = 'PFE10'
#     express10Comp2 = 'PFE10'
