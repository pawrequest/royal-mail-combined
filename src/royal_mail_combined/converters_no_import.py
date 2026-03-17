from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from royal_mail_combined.click_and_drop_api.models import CreateOrdersResponse
    from royal_mail_combined.parcels_apis.address.models import AddressVerified
    from royal_mail_combined.parcels_apis.collection_handler.models import GetAvailableSlotsResponse, SlotDateDef


def dps_postcode(verify_resp: AddressVerified) -> str:
    """Get DPS + postcode string from an address verify response."""
    return verify_resp.input.postcode.replace(" ", "") + verify_resp.dps


def created_orders_idents(created_order_response: CreateOrdersResponse) -> list[int]:
    return [_.order_identifier for _ in created_order_response.created_orders]


def created_orders_idents_str(created_order_response: CreateOrdersResponse) -> str:
    return ",".join(str(_) for _ in created_orders_idents(created_order_response))


def tracking_link(tracking_number: str) -> str:
    tlink = rf"https://www.royalmail.com/track-your-item#/tracking-results/{tracking_number}"
    return tlink


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


def match_collection_slot_date(slots: GetAvailableSlotsResponse, d: date) -> SlotDateDef | None:
    datewise = slots.task_slots.datewise_slots or ()
    return next((_ for _ in datewise if _.slot_date == d), None)


def order_idents_str(order_idents: list[str | int]) -> str:
    return ";".join([str(_) for _ in order_idents])
