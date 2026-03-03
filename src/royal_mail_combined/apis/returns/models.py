from royal_mail_combined import RMBaseModel
from royal_mail_combined.added_models.services import RoyalMailServiceCodes


class Service(RMBaseModel):
    service_code: RoyalMailServiceCodes


class CustomerReference(RMBaseModel):
    reference: str


class Address(RMBaseModel):
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
