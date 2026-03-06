from pydantic import Field

from royal_mail_combined import RMBaseModel
from royal_mail_combined.parcels_apis.collection_order.models.address_def import AddressDef


class AddressFindDPSRequest(RMBaseModel):
    addresses: list[AddressDef] = Field(..., alias='Addresses')


class AddressFindDPSResponse(RMBaseModel):
    input: AddressDef = Field(..., alias='Input')
    dps: str = Field(..., alias='DPS')

    @property
    def dps_postcode(self) -> str:
        return self.input.postcode.replace(' ', '') + self.dps
