from pydantic import Field, model_validator

from royal_mail_combined.core.consts_types import RoyalMailServiceCodes
from royal_mail_combined.core.rm_basemodel import RMBaseModel
from royal_mail_combined.parcels_apis.collection_order.models import CollectionOrderCreateResponse, SenderDetailsPostDef


class Service(RMBaseModel):
    service_code: RoyalMailServiceCodes


class CustomerReference(RMBaseModel):
    reference: str


class AddressReturns(RMBaseModel):
    title: str
    first_name: str
    last_name: str
    company_name: str | None = None
    address_line1: str
    address_line2: str | None = None
    address_line3: str | None = None
    city: str
    county: str | None = None
    postcode: str
    country: str
    country_iso_code: str = "GBR"
    email: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def details(self) -> SenderDetailsPostDef:
        return SenderDetailsPostDef(sender_name=self.full_name, sender_email=self.email)


class ReturnShipment(RMBaseModel):
    recipient_address: AddressReturns = Field(alias="shippingAddress")
    sender_address: AddressReturns = Field(alias="returnAddress")
    customer_reference: CustomerReference | None = None

    @model_validator(mode="after")
    def validate_customer_reference(self):
        if not self.customer_reference:
            ref = self.sender_address.company_name or self.sender_address.full_name
            self.customer_reference = CustomerReference(reference=ref)
        return self


class ReturnsRequest(RMBaseModel):
    service: Service
    shipment: ReturnShipment


class ReturnsResponseShipment(RMBaseModel):
    tracking_number: str
    unique_item_id: str


class ReturnsResponse(RMBaseModel):
    label: str
    qrCode: str
    shipment: ReturnsResponseShipment


class AvailableReturnService(RMBaseModel):
    carrier_guid: str
    carrier_service_guid: str
    service_name: str
    service_code: str


class AvailableServicesResponse(RMBaseModel):
    services: list[AvailableReturnService]

    def lookup_service_by_code(self, code: str) -> AvailableReturnService | None:
        for service in self.services:
            if service.service_code == code:
                return service
        return None


class ReturnResponseContainer(RMBaseModel):
    created_orders: list[ReturnsResponse]
    collection_response: CollectionOrderCreateResponse | None = None
