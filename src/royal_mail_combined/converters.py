from __future__ import annotations

from typing import Protocol

from royal_mail_combined.click_and_drop_api.models import AddressReturns

# from royal_mail_combined.all_models import (
#     AddressReturns,
#     AddressVerifable,
#     CreateOrdersResponse,
#     GetAvailableSlotsResponse,
#     SlotDateDef,
# )
from royal_mail_combined.parcels_apis.address.models.address import (
    AddressBasic,
    AddressDps,
    AddressVerifable,
)
from royal_mail_combined.parcels_apis.collection_order.models import SenderDetailsPostDef


class HasFullNameAndEmail(Protocol):
    @property
    def full_name(self) -> str: ...

    @property
    def email(self) -> str: ...


class HasFullNameAndEmail2(Protocol):
    full_name: str
    email: str


def details_from_address(sender: HasFullNameAndEmail) -> SenderDetailsPostDef:
    return SenderDetailsPostDef(sender_name=sender.full_name, sender_email=sender.email)


def rtn_address_to_addr_verify(address: AddressReturns) -> AddressVerifable:
    return AddressVerifable.model_validate(
        dict(
            address_line1=address.address_line1,
            address_line2=address.address_line2,
            address_line3=address.address_line3,
            post_town=address.city,
            county=address.county,
            postcode=address.postcode,
        )
    )


def addr_non_mandatory_from_addr(cached_address_verify: AddressVerifable) -> AddressBasic:
    return AddressBasic.model_validate(cached_address_verify, from_attributes=True)


def addr_mandatory_f_addr_and_dps(addr: AddressVerifable, dps: str):
    addr_mand = AddressDps(**addr.model_dump(), dps=dps)
    return addr_mand


def address_angonstic_to_verify_def(addr) -> AddressVerifable:
    data = addr.model_dump()
    if not data.get('postTown'):
        if data.get('city'):
            data['post_town'] = data['city']
        else:
            raise Exception('No post town or city provided for address - cannot convert to AddressVerifable')
    return AddressVerifable(
        address_line1=data.get('address_line1'),
        address_line2=data.get('address_line2'),
        address_line3=data.get('address_line3'),
        post_town=data.get('post_town'),
        county=data.get('county'),
        postcode=data.get('postcode'),
    )


def convert_address[T: type](addr, typ: T) -> T:
    data = addr.model_dump()
    if not data.get('postTown'):
        if data.get('city'):
            data['post_town'] = data['city']
        else:
            raise Exception('No post town or city provided for address - cannot convert to AddressVerifable')
    if typ is AddressVerifable:
        return typ(
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            address_line3=data.get('address_line3'),
            post_town=data.get('post_town'),
            county=data.get('county'),
            postcode=data.get('postcode'),
        )
    raise Exception(f'Unsupported type for address conversion: {typ}')
