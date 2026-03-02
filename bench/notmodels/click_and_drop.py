from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints, Field, StrictInt, conint, confloat, StrictStr, StrictBool, StrictFloat

from royal_mail_combined import RMBaseModel
from royal_mail_combined.models.consts_types import SendNotifcationsTo
from royal_mail_combined.models.services import RoyalMailServiceCodes

from royal_mail_combined.core.consts_types import PackageFormat


def str_length_constrained(length: int):
    return Annotated[
        str,
        StringConstraints(strip_whitespace=True, max_length=length),
    ]


class AddressRequest(RMBaseModel):
    full_name: str_length_constrained(210) = None
    company_name: str_length_constrained(100) | None = None
    address_line1: str_length_constrained(100)
    address_line2: str_length_constrained(100) | None = None
    address_line3: str_length_constrained(100) | None = None
    city: str_length_constrained(100)
    county: str_length_constrained(100) | None = None
    postcode: str_length_constrained(20) | None = None
    country_code: str_length_constrained(3) = 'GB'


class RecipientDetailsRequest(RMBaseModel):
    address: AddressRequest
    phone_number: Annotated[str, Field(strict=True, max_length=25)] | None = None
    email_address: Annotated[str, Field(strict=True, max_length=254)] | None = None
    address_book_reference: Annotated[str, Field(strict=True, max_length=100)] | None = Field(
        default=None,
        description='The presence or not of <b>addressBookReference</b> and a valid <b>recipient address object</b> in the request body will determine which of the following behaviours occur:-</br></br>1) addressBookReference <b>provided</b> and a valid recipient address object <b>provided</b> - In addition to the provided recipient address fields being used for the order creation, an existing account Address Book Reference with matching addressBookReference will be overwritten with all provided recipient address fields, including phone and email. If no existing account Address Book Reference with matching addressBookReference can be found then a new one will be created with the provided addressBookReference and address fields, including phone and email.</br>2) addressBookReference <b>provided</b> and a valid recipient address object <b>not provided</b> - An account Address Book Reference with the provided addressBookReference will be used for the order if it exists.</br>3) addressBookReference <b>not provided</b> and a valid recipient address object <b>provided</b> - All provided recipient address fields, including phone and email, will be used for the order creation.</br>4) All other scenarios will result in a validation error.',
    )


class DimensionsRequest(RMBaseModel):
    """
    It is not mandatory to include the dimensions field. If the dimensions field is included then the inner fields heightInMms, widthInMms and depthInMms must be specified with non-zero values.
    """

    height_in_mms: StrictInt
    width_in_mms: StrictInt
    depth_in_mms: StrictInt


class Importer(RMBaseModel):
    """
    Importer
    """

    company_name: Annotated[str, Field(strict=True, max_length=100)] | None = None
    address_line1: Annotated[str, Field(strict=True, max_length=100)] | None = None
    address_line2: Annotated[str, Field(strict=True, max_length=100)] | None = None
    address_line3: Annotated[str, Field(strict=True, max_length=100)] | None = None
    city: Annotated[str, Field(strict=True, max_length=100)] | None = None
    postcode: Annotated[str, Field(strict=True, max_length=20)] | None = None
    country: Annotated[str, Field(strict=True, max_length=100)] | None = None
    business_name: Annotated[str, Field(strict=True, max_length=100)] | None = None
    contact_name: Annotated[str, Field(strict=True, max_length=100)] | None = None
    phone_number: Annotated[str, Field(strict=True, max_length=25)] | None = None
    email_address: Annotated[str, Field(strict=True, max_length=254)] | None = None
    vat_number: Annotated[str, Field(strict=True, max_length=15)] | None = None
    tax_code: Annotated[str, Field(strict=True, max_length=25)] | None = None
    eori_number: Annotated[str, Field(strict=True, max_length=18)] | None = None


class ProductItemRequest(RMBaseModel):
    name: Annotated[str, Field(strict=True, max_length=800)] | None = None
    sku: Annotated[str, StringConstraints(strict=True, max_length=100)] | None = Field(
        default=None,
        description='The presence or not of field <b>SKU</b> and other fields in the request body will determine which of the following behaviours occur:- <br>1) A minimum of <b>SKU</b>, <b>unitValue</b>, <b>unitWeightInGrams</b> and <b>quantity</b> provided - In addition to the provided product fields being used for the order creation, an existing account Product with matching SKU will be overwritten with all provided product parameters. If no existing account Product with matching SKU can be found then a new product will be created with the provided SKU and product parameters.<br>2) <b>SKU</b>, <b>quantity</b> provided and <b>no other fields</b> provided - An account Product with the provided SKU will be used for the order if it exists.<br>3) <b>SKU not provided</b> and a minimum of <b>unitValue</b>, <b>unitWeightInGrams</b> and <b>quantity</b> provided - All provided product fields will be used for the order creation.<br>4) All other scenarios will result in a validation error.',
        alias='SKU',
    )
    quantity: conint(le=999999, strict=True, ge=1) = Field(description='The number of units in a given line')
    unit_value: (
        confloat(multiple_of=0.01, le=999999, strict=True, ge=0) | conint(le=999999, strict=True, ge=0) | None
    ) = Field(default=None, description='The price of a single unit excluding tax')
    unit_weight_in_grams: Annotated[int, Field(le=999999, strict=True, ge=0)] | None = Field(default=None)
    customs_description: Annotated[str, Field(strict=True, max_length=50)] | None = Field(default=None)
    extended_customs_description: Annotated[str, Field(strict=True, max_length=300)] | None = Field(default=None)
    customs_code: Annotated[str, Field(strict=True, max_length=10)] | None = Field(default=None)
    origin_country_code: Annotated[str, Field(strict=True, max_length=3)] | None = Field(default=None)
    customs_declaration_category: StrictStr | None = Field(default=None)
    requires_export_licence: StrictBool | None = Field(default=None)
    stock_location: Annotated[str, Field(strict=True, max_length=50)] | None = Field(default=None)
    use_origin_preference: StrictBool | None = None
    supplementary_units: Annotated[str, Field(strict=True, max_length=17)] | None = Field(default=None)
    license_number: Annotated[str, Field(strict=True, max_length=41)] | None = Field(default=None)
    certificate_number: Annotated[str, Field(strict=True, max_length=41)] | None = Field(default=None)


class ShipmentPackageRequest(RMBaseModel):
    weight_in_grams: Annotated[int, Field(le=30000, strict=True, ge=1)]
    package_format_identifier: PackageFormat = Field(
        description="<b>If you have a ChannelShipper account, you can also pass the name of any of your custom package formats instead of the values below.</b><br> Enum: 'undefined', 'letter', 'largeLetter', 'smallParcel', 'mediumParcel', 'parcel', 'documents'"
    )
    custom_package_format_identifier: StrictStr | None = Field(
        default=None,
        description="This field will be deprecated in the future. Please use 'packageFormatIdentifier' for custom package formats from ChannelShipper.",
    )
    dimensions: DimensionsRequest | None = None
    contents: list[ProductItemRequest] | None = None


class BillingDetailsRequest(RMBaseModel):
    """
    <b>Billing</b> along with <b>billing.address</b> objects are required in specific case when 'Use shipping address for billing address' setting is set to 'false' and 'Recipient.AddressBookReference' is provided.
    """

    address: AddressRequest | None = None
    phone_number: Annotated[str, Field(strict=True, max_length=25)] | None = None
    email_address: Annotated[str, Field(strict=True, max_length=254)] | None = None


class SenderDetailsRequest(RMBaseModel):
    trading_name: Annotated[str, Field(strict=True, max_length=250)] | None = None
    phone_number: Annotated[str, Field(strict=True, max_length=25)] | None = None
    email_address: Annotated[str, Field(strict=True, max_length=254)] | None = None


class PostageDetailsRequest(RMBaseModel):
    """
    PostageDetailsRequest
    """

    service_code: RoyalMailServiceCodes | None = None
    send_notifications_to: SendNotifcationsTo | None = None

    carrier_name: Annotated[str, Field(strict=True, max_length=50)] | None = None
    service_register_code: Annotated[str, Field(strict=True, max_length=2)] | None = None
    consequential_loss: Annotated[int, Field(le=10000, strict=True, ge=0)] | None = None
    receive_email_notification: StrictBool | None = None
    receive_sms_notification: StrictBool | None = None
    guaranteed_saturday_delivery: StrictBool | None = Field(default=None, description='This field has been deprecated')
    request_signature_upon_delivery: StrictBool | None = None
    is_local_collect: StrictBool | None = None
    safe_place: Annotated[str, Field(strict=True, max_length=90)] | None = None
    department: Annotated[str, Field(strict=True, max_length=150)] | None = None
    air_number: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None,
        description='For B2B orders shipping from Great Britain to Northern Ireland, this field can be used to provide the Recipient UKIMs number.',
    )
    ioss_number: Annotated[str, Field(strict=True, max_length=50)] | None = None
    requires_export_license: StrictBool | None = None
    commercial_invoice_number: Annotated[str, Field(strict=True, max_length=35)] | None = None
    recipient_eori_number: StrictStr | None = None
    commercial_invoice_date: datetime | None = None


class TagRequest(RMBaseModel):
    key: Annotated[str, Field(strict=True, max_length=100)] | None = None
    value: Annotated[str, Field(strict=True, max_length=100)] | None = None


class LabelGenerationRequest(RMBaseModel):
    """
    <b>Reserved for OBA customers only</b>
    """

    include_label_in_response: StrictBool
    include_cn: StrictBool | None = None
    include_returns_label: StrictBool | None = None


class CreateOrderRequest(RMBaseModel):
    recipient: RecipientDetailsRequest
    order_date: datetime
    subtotal: confloat(multiple_of=0.01, le=999999, strict=True, ge=0) | conint(le=999999, strict=True, ge=0) | None = (
        None
    )
    total: confloat(multiple_of=0.01, le=999999, strict=True, ge=0) | conint(le=999999, strict=True, ge=0) | None = None
    packages: list[ShipmentPackageRequest] | None = None
    billing: BillingDetailsRequest | None = None

    order_reference: str_length_constrained(40) | None = None
    planned_despatch_date: datetime | None = None
    sender: SenderDetailsRequest | None = None
    postage_details: PostageDetailsRequest | None = None

    is_recipient_a_business: StrictBool | None = Field(
        default=None,
        description='Indicates if the recipient is a business or not. Mandatory for Business senders on orders shipping from Great Britain to Northern Ireland, which require additional information for B2B shipments. (Business senders are OBA accounts and OLP accounts declaring themselves as a Business sender).',
    )
    special_instructions: Annotated[str, Field(strict=True, max_length=500)] | None = None
    shipping_cost_charged: (
        Annotated[float, Field(multiple_of=0.01, le=999999, strict=True, ge=0)]
        | Annotated[int, Field(le=999999, strict=True, ge=0)]
        | None
    ) = Field(default=None, description='The shipping costs you charged to your customer')  # todo is this optional?
    other_costs: (
        Annotated[float, Field(multiple_of=0.01, le=999999, strict=True, ge=0)]
        | Annotated[int, Field(le=999999, strict=True, ge=0)]
        | None
    ) = None
    customs_duty_costs: (
        Annotated[float, Field(multiple_of=0.01, le=99999.99, strict=True, ge=0)]
        | Annotated[int, Field(le=99999, strict=True, ge=0)]
        | None
    ) = Field(default=None, description='Customs Duty Costs is only supported in DDP (Delivery Duty Paid) services')
    currency_code: Annotated[str, Field(strict=True, max_length=3)] | None = None
    tags: list[TagRequest] | None = None
    label: LabelGenerationRequest | None = None
    order_tax: (
        Annotated[float, Field(multiple_of=0.01, le=999999, strict=True, ge=0)]
        | Annotated[int, Field(le=999999, strict=True, ge=0)]
        | None
    ) = Field(default=None, description='The total tax charged for the order')
    contains_dangerous_goods: StrictBool | None = Field(
        default=None, description='Indicates that the package contents contain a dangerous goods item'
    )
    dangerous_goods_un_code: Annotated[str, Field(strict=True, max_length=4)] | None = Field(
        default=None, description='UN Code of the dangerous goods'
    )
    dangerous_goods_description: Annotated[float, Field(strict=True)] | Annotated[int, Field(strict=True)] | None = (
        Field(default=None, description='Description of the dangerous goods')
    )
    dangerous_goods_quantity: StrictFloat | StrictInt | None = Field(
        default=None, description='Quantity or volume of the dangerous goods'
    )
    importer: Importer | None = None


class CreateOrdersRequest(RMBaseModel):
    orders: list[CreateOrderRequest]
