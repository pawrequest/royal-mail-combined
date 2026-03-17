from typing import Annotated

from pydantic import Field, StringConstraints, WithJsonSchema

from royal_mail_combined import RMBaseModel


class AddressDef(RMBaseModel):
    addressLine1: str
    addressLine2: str = ''
    addressLine3: str = ''
    postTown: str
    county: str = Field(None, alias='County')  # API spec has capital C here despite camelCase convention elsewhere
    postcode: str


class AddressFindRequest(RMBaseModel):
    """Address search string"""

    address_text: Annotated[
        str,
        StringConstraints(min_length=12, max_length=200),
        WithJsonSchema({'description': 'Address search string'}),
    ]


class AddressFindDPSRequest(RMBaseModel):
    # addresses: list[AddressDef]
    addresses: list[AddressDef] = Field(..., alias='Addresses')


class AddressFindDPSResponse(RMBaseModel):
    input: AddressDef = Field(..., alias='Input')
    dps: str = Field(..., alias='DPS')

    @property
    def dps_postcode(self) -> str:
        return self.input.postcode.replace(' ', '') + self.dps


class AddressSummary(RMBaseModel):
    address_id: Annotated[
        str,
        WithJsonSchema({'description': 'Unique identifier for address record retrieval'}),
    ]
    address_summary1: str = ''
    address_summary2: str = ''
    type: str = ''
    highlight: str = ''


class AddressSearchResponse(RMBaseModel):
    addresses: list[AddressSummary] = Field(default_factory=list)


class AddressRecord(RMBaseModel):
    # model_config = ConfigDict(
    #     coerce_numbers_to_str=True
    # )
    address_id: str = ''
    domestic_id: str = ''
    language: str = ''
    language_alternatives: str = ''
    department: str = ''
    company: str = ''
    sub_building: str = ''
    building_number: str = ''
    building_name: str = ''
    secondary_street: str = ''
    street: str = ''
    block: str = ''
    neighbourhood: str = ''
    district: str = ''
    city: str = ''
    line1: str = ''
    line2: str = ''
    line3: str = ''
    line4: str = ''
    line5: str = ''
    admin_area_name: str = ''
    admin_area_code: str = ''
    province: str = ''
    province_name: str = ''
    province_code: str = ''
    postal_code: str = ''
    country_name: str = ''
    country_iso2: str = ''
    country_iso3: str = ''
    country_iso_number: int | None = None
    sorting_number1: str = ''
    sorting_number2: str = ''
    barcode: str = ''
    po_box_number: str = ''
    label: str = ''
    type: str = ''
    data_level: str = ''
