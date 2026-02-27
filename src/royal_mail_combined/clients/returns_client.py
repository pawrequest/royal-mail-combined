from royal_mail_combined import RMBaseModel
from royal_mail_combined.click_and_drop.services import RoyalMailServiceCodeClickDrop
from royal_mail_combined.clients._base_client import _RMBaseClient

RETURNS_ENDPOINT = r'https://api.parcel.royalmail.com/api/v1/returns'


class Service(RMBaseModel):
    service_code: RoyalMailServiceCodeClickDrop


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


class ReturnsClient(_RMBaseClient):
    def create_return(self, return_request: ReturnsRequest | dict):
        resp = self._do_post(url=RETURNS_ENDPOINT, data=return_request, headers=self.settings.headers_bearer())
        ...
