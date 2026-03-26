from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, Field

from royal_mail_combined.core import RMBaseModel


class AddressRecordDefPermissive(RMBaseModel):
    address_id: str | None = Field(
        default=None, description='Unique identifier for address record retrieval', alias='addressId'
    )
    domestic_id: str | None = Field(default=None, description='Domestic ID', alias='DomesticId')
    language: str | None = Field(default=None, description='Language of the result', alias='Language')
    language_alternatives: str | None = Field(
        default=None, description='Available language alternatives', alias='LanguageAlternatives'
    )
    department: str | None = Field(default=None, description='Department', alias='Department')
    company: str | None = Field(default=None, description='Company name', alias='Company')
    sub_building: str | None = Field(default=None, description='Building name', alias='SubBuilding')
    building_number: str | None = Field(default=None, description='Building number', alias='BuildingNumber')
    building_name: str | None = Field(default=None, description='Building name', alias='BuildingName')
    secondary_street: str | None = Field(default=None, description='Secondary Street name', alias='SecondaryStreet')
    street: str | None = Field(default=None, description='Street name', alias='Street')
    block: str | None = Field(default=None, description='block number', alias='Block')
    neighbourhood: str | None = Field(default=None, description='Neighbourhood name', alias='Neighbourhood')
    district: str | None = Field(default=None, description='District name', alias='District')
    city: str | None = Field(default=None, description='City name', alias='City')
    line1: str | None = Field(default=None, description='Address Line 1', alias='Line1')
    line2: str | None = Field(default=None, description='Address Line 2', alias='Line2')
    line3: str | None = Field(default=None, description='Address Line 3', alias='Line3')
    line4: str | None = Field(default=None, description='Address Line 4', alias='Line4')
    line5: str | None = Field(default=None, description='Address Line 5', alias='Line5')
    admin_area_name: str | None = Field(default=None, description='Admin area', alias='AdminAreaName')
    admin_area_code: str | None = Field(default=None, description='Admin area code', alias='AdminAreaCode')
    province: str | None = Field(default=None, description='Province', alias='Province')
    province_name: str | None = Field(default=None, description='ProvinceName', alias='ProvinceName')
    province_code: str | None = Field(default=None, description='Province Code', alias='ProvinceCode')
    postal_code: str | None = Field(default=None, description='Postal Code', alias='PostalCode')
    country_name: str | None = Field(default=None, description='Country Name', alias='CountryName')
    country_iso2: str | None = Field(default=None, description='2 digit Country Iso code', alias='CountryIso2')
    country_iso3: str | None = Field(default=None, description='3 digit Country Iso code', alias='CountryIso3')
    country_iso_number: Annotated[str, BeforeValidator(lambda v: str(v))] | None = Field(
        default=None, description='Country Iso Number', alias='CountryIsoNumber'
    )
    sorting_number1: str | None = Field(default=None, description='Sorting Number 1', alias='SortingNumber1')
    sorting_number2: str | None = Field(default=None, description='Sorting Number 2', alias='SortingNumber2')
    barcode: str | None = Field(default=None, description='Barcode with DPS', alias='Barcode')
    po_box_number: str | None = Field(default=None, description='PO Box Number', alias='POBoxNumber')
    label: str | None = Field(default=None, description='Label', alias='Label')
    type: str | None = Field(default=None, description='Type', alias='Type')
    data_level: str | None = Field(default=None, description='Data Level', alias='DataLevel')
