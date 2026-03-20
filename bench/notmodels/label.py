from __future__ import annotations

from datetime import date
from typing import Annotated

from pydantic import Field, NonNegativeInt, StrictFloat, StrictInt, StrictStr, StringConstraints

from royal_mail_combined import RMBaseModel
from royal_mail_combined.models.consts_types import OptionalStrictNumber


class LabelOrderItem(RMBaseModel):
    """
    LabelOrderItem
    """

    description: Annotated[str | None, StringConstraints(strict=True, max_length=50)] = None
    customs_code: Annotated[str | None, StringConstraints(strict=True, max_length=12)] = None
    quantity: StrictInt | None = None
    unit_value: OptionalStrictNumber = None
    unit_weight_in_grams: StrictInt | None = Field(default=None, alias='unitWeightInGrams')
    origin_country_code: Annotated[str | None, StringConstraints(strict=True, max_length=3)] = None


class LabelAddress(RMBaseModel):
    """
    LabelAddress
    """

    name: Annotated[str | None, StringConstraints(strict=True, max_length=50)] = None
    company_name: Annotated[str | None, StringConstraints(strict=True, max_length=50)]
    address_line1: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=64)]
    address_line2: Annotated[str | None, StringConstraints(strict=True, max_length=64)] = None
    address_line3: Annotated[str | None, Field(strict=True, max_length=64)] = None
    post_town: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=64)]
    county: Annotated[str | None, StringConstraints(strict=True, max_length=64)] = None
    postcode: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=10)]
    dps: Annotated[str | None, StringConstraints(strict=True, max_length=10)] = Field(default='9Z', alias='DPS')
    country_code: Annotated[str, StringConstraints(strict=True, max_length=3)] = 'GBR'


class LabelCustomsInfo(RMBaseModel):
    """
    LabelCustomsInfo
    """

    currency_code: Annotated[str | None, StringConstraints(strict=True, max_length=3)] = None
    total_cost: OptionalStrictNumber = None
    shipment_subtotal: OptionalStrictNumber = None
    shipping_cost_charged: OptionalStrictNumber = Field(default=None, alias='shippingCostCharged')
    customs_duty_cost: OptionalStrictNumber = None
    ioss_number: Annotated[str, StringConstraints(strict=True, max_length=20)] = Field(default=None, alias='IOSSNumber')
    air_number: Annotated[str, StringConstraints(strict=True, max_length=20)] = Field(default=None, alias='AIRNumber')
    customs_declaration_category: StrictStr | None = None
    contents: list[LabelOrderItem] = Field(default_factory=list)


class LabelInfo(RMBaseModel):
    """
    LabelInfo
    """

    var_1_d_tracking_number: Annotated[str | None, StringConstraints(strict=True, max_length=13)] = Field(
        default=None, alias='1DTrackingNumber'
    )
    var_2_d_unique_identifier: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=21)] = Field(
        alias='2DUniqueIdentifier'
    )
    post_by_date: date
    rm_service: Annotated[str, StringConstraints(min_length=1, strict=True, max_length=50)] = Field(alias='RMService')
    price_paid: StrictFloat | StrictInt
    reference_number: Annotated[str | None, StringConstraints(strict=True, max_length=20)] = None
    reference_text: Annotated[str | None, StringConstraints(strict=True, max_length=40)]
    weight_in_grams: NonNegativeInt
    item_format: StrictStr
    recipient_address: LabelAddress = Field(alias='recipientAddress')
    sender_address: LabelAddress = Field(alias='senderAddress')
    customs_info: LabelCustomsInfo | None = None
