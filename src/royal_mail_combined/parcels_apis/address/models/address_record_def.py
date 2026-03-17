from __future__ import annotations

import re  # noqa: F401
from typing import Annotated

from pydantic import BeforeValidator, Field

from royal_mail_combined.core import RMBaseModel


class AddressRecordDef(RMBaseModel):
    """
    Full and detailed address record as available in the address store
    """

    address_id: Annotated[str, Field(strict=True, max_length=256)] | None = Field(
        default=None,
        description='Unique identifier for address record retrieval',
        alias='addressId',
    )
    domestic_id: Annotated[str, Field(strict=True, max_length=256)] | None = Field(
        default=None, description='Domestic ID', alias='DomesticId'
    )
    language: Annotated[str, Field(strict=True, max_length=10)] | None = Field(
        default=None, description='Language of the result', alias='Language'
    )
    language_alternatives: Annotated[str, Field(strict=True, max_length=10)] | None = Field(
        default=None, description='Available language alternatives', alias='LanguageAlternatives'
    )
    department: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Department', alias='Department'
    )
    company: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Company name', alias='Company'
    )
    sub_building: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Building name', alias='SubBuilding'
    )
    building_number: Annotated[str, Field(strict=True, max_length=10)] | None = Field(
        default=None, description='Building number', alias='BuildingNumber'
    )
    building_name: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Building name', alias='BuildingName'
    )
    secondary_street: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Secondary Street name', alias='SecondaryStreet'
    )
    street: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Street name', alias='Street'
    )
    block: Annotated[str, Field(strict=True, max_length=10)] | None = Field(
        default=None, description='block number', alias='Block'
    )
    neighbourhood: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Neighbourhood name', alias='Neighbourhood'
    )
    district: Annotated[str, Field(strict=True, max_length=20)] | None = Field(
        default=None, description='District name', alias='District'
    )
    city: Annotated[str, Field(strict=True, max_length=20)] | None = Field(
        default=None, description='City name', alias='City'
    )
    line1: Annotated[str, Field(strict=True, max_length=100)] | None = Field(
        default=None, description='Address Line 1', alias='Line1'
    )
    line2: Annotated[str, Field(strict=True, max_length=100)] | None = Field(
        default=None, description='Address Line 2', alias='Line2'
    )
    line3: Annotated[str, Field(strict=True, max_length=100)] | None = Field(
        default=None, description='Address Line 3', alias='Line3'
    )
    line4: Annotated[str, Field(strict=True, max_length=100)] | None = Field(
        default=None, description='Address Line 4', alias='Line4'
    )
    line5: Annotated[str, Field(strict=True, max_length=100)] | None = Field(
        default=None, description='Address Line 5', alias='Line5'
    )
    admin_area_name: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Admin area', alias='AdminAreaName'
    )
    admin_area_code: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Admin area code', alias='AdminAreaCode'
    )
    province: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Province', alias='Province'
    )
    province_name: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='ProvinceName', alias='ProvinceName'
    )
    province_code: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Province Code', alias='ProvinceCode'
    )
    postal_code: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Postal Code', alias='PostalCode'
    )
    country_name: Annotated[str, Field(strict=True, max_length=50)] | None = Field(
        default=None, description='Country Name', alias='CountryName'
    )
    country_iso2: Annotated[str, Field(max_length=2)] | None = Field(
        default=None, description='2 digit Country Iso code', alias='CountryIso2'
    )
    country_iso3: Annotated[str, Field(max_length=3)] | None = Field(
        default=None, description='3 digit Country Iso code', alias='CountryIso3'
    )
    country_iso_number: Annotated[str, BeforeValidator(lambda v: str(v)), Field(max_length=10)] | None = Field(
        default=None, description='Country Iso Number', alias='CountryIsoNumber'
    )
    sorting_number1: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Sorting Number 1', alias='SortingNumber1'
    )
    sorting_number2: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Sorting Number 2', alias='SortingNumber2'
    )
    barcode: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Barcode with DPS', alias='Barcode'
    )
    po_box_number: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='PO Box Number', alias='POBoxNumber'
    )
    label: Annotated[str, Field(strict=True, max_length=200)] | None = Field(
        default=None, description='Label', alias='Label'
    )
    type: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Type', alias='Type'
    )
    data_level: Annotated[str, Field(strict=True, max_length=30)] | None = Field(
        default=None, description='Data Level', alias='DataLevel'
    )
