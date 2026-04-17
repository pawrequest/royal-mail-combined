from __future__ import annotations

import re  # noqa: F401
from datetime import datetime
from typing import Annotated

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr

from royal_mail_combined.core import RMBaseModel

from ...core.consts_types import StrictNonNegativeNumber
from ..models.billing_details_request import BillingDetailsRequest
from ..models.importer import Importer
from ..models.label_generation_request import LabelGenerationRequest
from ..models.postage_details_request import PostageDetailsRequest
from ..models.recipient_details_request import RecipientDetailsRequest
from ..models.sender_details_request import SenderDetailsRequest
from ..models.shipment_package_request import ShipmentPackageRequest
from ..models.tag_request import TagRequest


class CreateOrderRequest(RMBaseModel):
    recipient: RecipientDetailsRequest
    packages: list[ShipmentPackageRequest]
    order_date: datetime

    sender: SenderDetailsRequest | None = None
    billing: BillingDetailsRequest | None = None
    order_reference: StrictStr | None = None
    is_recipient_a_business: StrictBool | None = None
    planned_despatch_date: datetime | None = None
    special_instructions: Annotated[str, Field(strict=True, max_length=500)] | None = None
    subtotal: StrictNonNegativeNumber = Field(
        default=0,
        description='The total value of all the goods in the order, excluding tax. This should not include retail shipping costs',
    )
    shipping_cost_charged: StrictNonNegativeNumber = Field(
        default=0, description='The shipping costs you charged to your customer', alias='shippingCostCharged'
    )
    other_costs: StrictNonNegativeNumber | None = Field(default=None, alias='otherCosts')
    customs_duty_costs: StrictNonNegativeNumber | None = Field(
        default=None,
        description='Customs Duty Costs is only supported in DDP (Delivery Duty Paid) services',
    )
    total: StrictNonNegativeNumber = Field(
        default=0, description='The sum of order subtotal, tax and retail shipping costs'
    )
    currency_code: Annotated[str, Field(strict=True, max_length=3)] | None = Field(default=None, alias='currencyCode')
    postage_details: PostageDetailsRequest | None = Field(default=None, alias='postageDetails')
    tags: list[TagRequest] | None = None
    label: LabelGenerationRequest | None = None
    order_tax: StrictNonNegativeNumber | None = Field(
        default=None, description='The total tax charged for the order', alias='orderTax'
    )
    contains_dangerous_goods: StrictBool | None = Field(
        default=None,
        description='Indicates that the package contents contain a dangerous goods item',
        alias='containsDangerousGoods',
    )
    dangerous_goods_un_code: Annotated[str, Field(strict=True, max_length=4)] | None = Field(
        default=None, description='UN Code of the dangerous goods', alias='dangerousGoodsUnCode'
    )
    dangerous_goods_description: Annotated[float, Field(strict=True)] | Annotated[int, Field(strict=True)] | None = (
        Field(
            default=None,
            description='Description of the dangerous goods',
            alias='dangerousGoodsDescription',
        )
    )
    dangerous_goods_quantity: StrictFloat | StrictInt | None = Field(
        default=None,
        description='Quantity or volume of the dangerous goods',
        alias='dangerousGoodsQuantity',
    )
    importer: Importer | None = None

    def add_label_request(self):
        if not self.label:
            self.label = LabelGenerationRequest(include_label_in_response=True)
        if not self.label.include_label_in_response:
            self.label.include_label_in_response = True
