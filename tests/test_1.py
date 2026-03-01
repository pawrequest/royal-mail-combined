import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import pytest

from royal_mail_combined.apis.parcels_apis.address.models import (
    AddressRecordDef,
    AddressVerifyDef,
    AddressVerifyReqRespdef,
    AddressVerifyRequestDef,
    AddressesDef,
)
from royal_mail_combined.apis.click_and_drop.models import GetOrdersResponse
from royal_mail_combined.apis.parcels_apis.collection_handler.models import GetAvailableSlotsResponse, SlotDateDef
from royal_mail_combined.apis.parcels_apis.collection_order.models import (
    AddressNonMandatoryDef,
    Collection,
    CollectionItemType,
    DimensionsPostDef,
    ItemsPostDef,
)
from royal_mail_combined.apis.returns.models import ReturnsResponse

TEST_DATE = date.today() + timedelta(days=2)

STORE_RESULTS = True


def dump_result(result: dict | list[dict], results_file):
    results_file.parent.mkdir(parents=True, exist_ok=True)
    results_json = json.dumps(result)
    results_file.write_text(results_json)


# @pytest.mark.skip(reason='Use Cached result')
def test_address_search(sample_client, sample_address):
    search_str = sample_address.address_line1 + ', ' + sample_address.postcode
    resp: AddressesDef = sample_client.parcel_api.address_search(search_str)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/address_search_results.json')
        dump_result(result, results_file)

    assert isinstance(resp, AddressesDef)
    ...


@pytest.mark.skip(reason='Use Cached')
def test_address_search_dps(sample_client, sample_address):
    addr = AddressVerifyDef.model_validate(sample_address, from_attributes=True)
    addresses_payload = AddressVerifyRequestDef(addresses=[addr])
    resp: list[AddressVerifyReqRespdef] = sample_client.address_search_verify(addresses_payload)
    if STORE_RESULTS:
        result = [_.model_dump(mode='json') for _ in resp]
        results_file = Path('data/address_search_dps_results.json')
        dump_result(result, results_file)

    assert isinstance(resp, list)
    assert isinstance(resp[0], AddressVerifyReqRespdef)


@pytest.mark.skip(reason='Use Cached result')
def test_address_get(sample_client, sample_address_id):
    resp = sample_client.address_fetch(sample_address_id)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/address_get_result.json')
        dump_result(result, results_file)
    assert isinstance(resp, AddressRecordDef)


@pytest.mark.skip(reason='Use Cached result')
def test_handler_get_slots(sample_client, sample_dps_results):
    dps = sample_dps_results.dps
    postcode = sample_dps_results.input.postcode.replace(' ', '')
    dps_postcode = postcode + dps
    item_count = 1
    resp = sample_client.parcel_api.slots_get_available(dps_postcode, item_count)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/collection_order_handler_get_slots.json')
        dump_result(result, results_file)
    assert isinstance(resp, GetAvailableSlotsResponse)


def test_my_slot(sample_slots_response):
    send_date = date.today() + timedelta(days=3)
    myslot = sample_slots_response.match_date(send_date)
    assert isinstance(myslot, SlotDateDef)


def match_date(slots: GetAvailableSlotsResponse, d: date) -> SlotDateDef | None:
    datewise = slots.task_slots.datewise_slots or ()
    return next((_ for _ in datewise if _.slot_date == d), None)


# @pytest.mark.skip(reason='blah')
def test_inbound_booking_story(
        sample_address_verify,
        sample_client,
        sample_sender,
        sample_account_details,
):
    # get DPS
    dps_request = AddressVerifyRequestDef(addresses=[sample_address_verify])
    dps_responses = sample_client.parcel_api.address_verify(dps_request)
    dps_response = dps_responses[0]

    # get collection slot
    item_count = 1
    slots_response = sample_client.parcel_api.slots_get_available(dps=dps_response.dps_postcode, item_count=item_count)
    my_slot = match_date(slots_response, TEST_DATE)
    if my_slot is None:
        raise Exception('No slot found for date')
    token = slots_response.task_slots.slot_details.token_id
    ...
    barcode = 'GET BACODE!!'
    dims = DimensionsPostDef(height=30, width=30, depth=30)
    item = ItemsPostDef(
        item_barcode_id=barcode,
        weight_in_grams=10000,
        item_service_name='Royal Mail Tracked 24',
        item_type=CollectionItemType.STANDARD,
        dimensions=dims,
    )

    # book collection
    collection_payload = Collection(
        timeslot_reservation_id=token,
        sender_details=sample_sender,
        account_details=sample_account_details,
        address=AddressNonMandatoryDef.model_validate(sample_address_verify, from_attributes=True),
        collection_date=TEST_DATE,
        items=[item],
    )

    order_resp = sample_client.parcel_api.collection_create(collection=collection_payload)
    ...


@pytest.mark.skip(reason='unable to cancel?')
def test_returns(sample_return_request, sample_client):
    resp = sample_client.create_return_shipment_order(sample_return_request)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/create_return_shipment_order_result.json')
        dump_result(result, results_file)
    assert isinstance(resp, ReturnsResponse)
    ...


def test_fetch_orders(sample_client):
    res = sample_client.click_and_drop.fetch_orders()
    if STORE_RESULTS:
        result = res.model_dump(mode='json')
        results_file = Path('data/fetch_orders_result.json')
        dump_result(result, results_file)
    assert isinstance(res, GetOrdersResponse)
    ...


def test_fetch_specific(sample_client):
    tracking_number = "ZS191785025GB"
    unique_item_id = "32073580900070AD6B7F8"
    track2 = 'PK007810419GB'
    anitem = 1037
    # idents = quote(tracking_number)
    # idents = quote(f'"{anitem}"')
    idents = quote(str(anitem))
    res = sample_client.click_and_drop.fetch_specific(order_identifiers=idents)
    if STORE_RESULTS:
        result = res[0].model_dump(mode='json')
        results_file = Path('data/fetch_specific_result.json')
        dump_result(result, results_file)
    ...
    # ident = '32073580900070AD6B7F8' # uniquesItemId from returns endpoint
    # sample_client.label_data_fetch(order_idents=ident)
    ...

    # book return
    # fetch order info
    # use info to book collection
    # cancel collection
    ...
