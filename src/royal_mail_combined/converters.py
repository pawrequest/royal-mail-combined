from datetime import date
from urllib.parse import quote
import base64

from royal_mail_combined.apis.click_and_drop.models import (
    CreateOrderRequest,
    CreateOrdersResponse,
    LabelGenerationRequest,
)
from royal_mail_combined.apis.parcels_apis.collection_handler.models import GetAvailableSlotsResponse, SlotDateDef
from royal_mail_combined.apis.parcels_apis.collection_order.models import AddressMandatoryDef, AddressNonMandatoryDef
from royal_mail_combined.apis.returns.models import Address
from royal_mail_combined.apis.parcels_apis.address.models import AddressVerifyDef, AddressVerifyReqRespdef


def rtn_address_to_addr_verify(address: Address) -> AddressVerifyDef:
    return AddressVerifyDef.model_validate(
        dict(
            address_line1=address.address_line1,
            address_line2=address.address_line2,
            address_line3=address.address_line3,
            post_town=address.city,
            county=address.county,
            postcode=address.postcode,
        )
    )


def address_angonstic_to_verify_def(addr) -> AddressVerifyDef:
    data = addr.model_dump()
    if not data.get('postTown'):
        if data.get('city'):
            data['post_town'] = data['city']
    return AddressVerifyDef(
        address_line1=data.get('address_line1'),
        address_line2=data.get('address_line2'),
        address_line3=data.get('address_line3'),
        post_town=data.get('post_town'),
        county=data.get('county'),
        postcode=data.get('postcode'),
    )


def dps_postcode(verify_resp: AddressVerifyReqRespdef) -> str:
    return verify_resp.input.postcode.replace(' ', '') + verify_resp.dps


def addr_non_mandatory_from_addr(cached_address_verify: AddressVerifyDef) -> AddressNonMandatoryDef:
    return AddressNonMandatoryDef.model_validate(cached_address_verify, from_attributes=True)


def addr_mandatory_f_addr_and_dps(addr: AddressVerifyDef, dps: str):
    addr_mand = AddressMandatoryDef(
        **addr.model_dump(),
        dps=dps,
    )
    return addr_mand


def created_orders_idents(created_order_response: CreateOrdersResponse) -> list[int]:
    return [_.order_identifier for _ in created_order_response.created_orders]


def created_orders_idents_str(created_order_response: CreateOrdersResponse) -> str:
    return ','.join(str(_) for _ in created_orders_idents(created_order_response))


def tracking_link(tracking_number: str) -> str:
    tlink = fr'https://www.royalmail.com/track-your-item#/tracking-results/{tracking_number}'
    return tlink


def add_label_gen_request(*orders: CreateOrderRequest):
    orders = list(orders)
    for order in orders:
        if not order.label:
            order.label = LabelGenerationRequest(include_label_in_response=True)
        if not order.label.include_label_in_response:
            order.label.include_label_in_response = True


def order_identifier_to_string(id_or_ref: int | str) -> str:
    if isinstance(id_or_ref, int):
        return str(id_or_ref)
    elif isinstance(id_or_ref, str):
        return f'"{quote(id_or_ref)}"'
    raise TypeError(f"Expected int or str, got {id_or_ref}.")


def order_identifiers_to_string(
        order_identifiers: list[str | int] | str | int,
) -> str:
    """Encode order ids and references."""
    if not isinstance(order_identifiers, list):
        order_identifiers = [order_identifiers]
    return ";".join(map(order_identifier_to_string, order_identifiers))


def match_date(slots: GetAvailableSlotsResponse, d: date) -> SlotDateDef | None:
    datewise = slots.task_slots.datewise_slots or ()
    return next((_ for _ in datewise if _.slot_date == d), None)


def decode_b64(s: str) -> bytes:
    return base64.b64decode(s)
