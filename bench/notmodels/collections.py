from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import Field, NonNegativeInt, StrictFloat, StrictInt, StrictStr, StringConstraints
from typing import Annotated

from royal_mail_combined import RMBaseModel
from royal_mail_combined.apis.parcels_apis.collection_order import LabelInfo


class SenderDetailsPostDef(RMBaseModel):
    """
    SenderDetailsPostDef
    """

    sender_name: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=100)]
    sender_email: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=50)]


class AccountDetailsDef(RMBaseModel):
    """
    account details definition
    """

    partner_id: Annotated[str | None, StringConstraints(strict=True, max_length=20)] = None
    retailer_account_number: Annotated[str | None, Field(strict=True, max_length=10)] = None


class AddressNonMandatoryDef(RMBaseModel):
    """
    account details definition
    """

    address_line1: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=64)]
    address_line2: Annotated[str | None, StringConstraints(strict=True, max_length=64)] = None
    address_line3: Annotated[str | None, StringConstraints(strict=True, max_length=64)] = None
    post_town: Annotated[str | None, StringConstraints(min_length=0, strict=True, max_length=64)] = None
    postcode: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=10)]
    dps: Annotated[str | None, StringConstraints(min_length=0, strict=True, max_length=10)] = None
    county: Annotated[str | None, StringConstraints(strict=True, max_length=64)] = None


class SafePlaceDetailsDef(RMBaseModel):
    """
    safe place details definition
    """

    location_text: Annotated[str | None, StringConstraints(strict=True, max_length=50)] = None
    location_code: Annotated[str | None, StringConstraints(strict=True, max_length=10)] = None


class DimensionsPostDef(RMBaseModel):
    """
    DimensionsPostDef
    """

    height: StrictFloat | StrictInt
    width: StrictFloat | StrictInt
    depth: StrictFloat | StrictInt


class CollectionItemType(StrEnum):
    STANDARD = 'Standard'
    NOLABEL = 'NoLabel'
    NOPACKAGE = 'NoPackage'


class ItemsPostDef(RMBaseModel):
    """
    items detail definition
    """

    item_barcode_id: Annotated[str | None, StringConstraints(min_length=1, strict=True, max_length=21)] = None
    item_reference: Annotated[str | None, StringConstraints(strict=True, max_length=40)] = None
    weight_in_grams: NonNegativeInt
    item_service_name: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=50)]
    item_status: StrictStr = 'AwaitingCollection'
    dimensions: DimensionsPostDef
    item_price: StrictFloat | StrictInt | None = None
    item_type: CollectionItemType | None = None
    item_product_code: Annotated[str | None, StringConstraints(strict=True, max_length=5)] = None
    label_info: LabelInfo | None = None


class Collection(RMBaseModel):
    timeslot_reservation_id: Annotated[str | None, StringConstraints(min_length=0, strict=True, max_length=64)] = Field(
        default=None, description='time slot reservation Id', alias='timeslotReservationId'
    )
    sender_details: SenderDetailsPostDef = Field(alias='senderDetails')
    account_details: AccountDetailsDef = Field(alias='accountDetails')
    address: AddressNonMandatoryDef
    collection_date: date
    items: list[ItemsPostDef]
    safe_place_details: SafePlaceDetailsDef | None = None
    animal_hazard_details: Annotated[str | None, StringConstraints(max_length=50)] = None
    suppress_rm_notifications: bool | None = None
