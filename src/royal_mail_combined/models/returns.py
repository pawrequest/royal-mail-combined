from royal_mail_combined import RMBaseModel
from royal_mail_combined.models.services import RoyalMailServices26

RETURNS_ENDPOINT = r'https://api.parcel.royalmail.com/api/v1/returns'


class Service(RMBaseModel):
    service_code: RoyalMailServices26


class CustomerReference(RMBaseModel):
    reference: str


class Address(RMBaseModel):
    title: str
    first_name: str
    last_name: str
    company_name: str | None
    address_line_1: str
    address_line_2: str | None
    address_line_3: str | None
    city: str
    county: str | None
    postcode: str
    country: str
    country_iso_code: str


class Shipment(RMBaseModel):
    shipping_address: Address
    return_address: Address
    customer_reference: CustomerReference | None = None


class ReturnsRequest(RMBaseModel):
    service: Service
    shipment: Shipment


class ReturnsResponseShipment(RMBaseModel):
    tracking_number: str
    unique_item_id: str


class ReturnsResponse(RMBaseModel):
    label: str
    qrCode: str
    shipment: ReturnsResponseShipment
