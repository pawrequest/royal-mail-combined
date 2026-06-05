from pydantic import Field, field_validator, model_validator

from royal_mail_combined.core.consts_types import RoyalMailServiceCodes
from royal_mail_combined.core.endpoints import tracking_link
from royal_mail_combined.core.rm_basemodel import RMBaseModel
from royal_mail_combined.parcels_apis.collection_order.models import CollectionOrderCreateResponse, SenderDetailsPostDef


class Service(RMBaseModel):
    service_code: RoyalMailServiceCodes
    service_register_code: str = Field(default='01', alias='ServiceRegisterCode')


class CustomerReference(RMBaseModel):
    reference: str


class AddressReturns(RMBaseModel):
    title: str
    first_name: str
    last_name: str
    company_name: str = ''
    address_line1: str
    address_line2: str = ''
    address_line3: str = ''
    city: str
    county: str = ''
    postcode: str
    country: str
    country_iso_code: str = 'GBR'
    email: str

    @field_validator('county', 'address_line2', 'address_line3', 'company_name')
    def empty_string_nones(cls, v):
        return v or ''

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def details(self) -> SenderDetailsPostDef:
        return SenderDetailsPostDef(sender_name=self.full_name, sender_email=self.email)


class ReturnShipment(RMBaseModel):
    recipient_address: AddressReturns = Field(alias='shippingAddress')
    sender_address: AddressReturns = Field(alias='returnAddress')
    customer_reference: CustomerReference | None = None

    @model_validator(mode='after')
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


class ReturnRequestContainer(RMBaseModel):
    return_requests: list[ReturnsRequest]

    @property
    def service_code(self) -> str:
        return self.return_requests[0].service.service_code

    @property
    def recipient_address(self) -> AddressReturns:
        return self.return_requests[0].shipment.recipient_address

    @property
    def sender_address(self) -> AddressReturns:
        return self.return_requests[0].shipment.sender_address

    @field_validator('return_requests', mode='after')
    def validate_return_requests_single_service_sender_recip(cls, v):
        item1_service = v[0].service.service_code
        item1_recip = v[0].shipment.recipient_address
        item1_sender = v[0].shipment.sender_address
        for req in v:
            if req.service.service_code != item1_service:
                raise ValueError('All return requests must have the same service code')
            if req.shipment.recipient_address != item1_recip:
                raise ValueError('All return requests must have the same recipient address')
            if req.shipment.sender_address != item1_sender:
                raise ValueError('All return requests must have the same sender address')
        return v


class ReturnResponseContainer(RMBaseModel):
    created_orders: list[ReturnsResponse]
    collection_response: CollectionOrderCreateResponse | None = None

    @property
    def tracking_numbers(self) -> list[str]:
        return [order.shipment.tracking_number for order in self.created_orders]

    @property
    def unique_ids(self) -> list[str]:
        return [order.shipment.unique_item_id for order in self.created_orders]

    @property
    def unique_ids_str(self) -> str:
        return ';'.join(self.unique_ids)

    @property
    def tracking_links(self) -> list[str]:
        return [tracking_link(_) for _ in self.tracking_numbers]
