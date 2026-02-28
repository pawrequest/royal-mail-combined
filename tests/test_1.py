import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from royal_mail_combined.models.address import (
    AddressFindDPSRequest,
    AddressFindDPSResponse,
    AddressRecord,
    AddressSummary,
)
from royal_mail_combined.models.responses import GetOrdersResponse
from royal_mail_combined.models.returns import ReturnsResponse
from royal_mail_combined.models.collections import (
    AddressNonMandatoryDef,
    Collection,
    CollectionItemType,
    DimensionsPostDef,
    GetAvailableSlotsResponse,
    ItemsPostDef,
    SlotDateDef,
)

STORE_RESULTS = False


def dump_result(result: dict | list[dict], results_file):
    results_file.parent.mkdir(parents=True, exist_ok=True)
    results_json = json.dumps(result)
    results_file.write_text(results_json)


# @pytest.mark.skip(reason='Use Cached result')
def test_address_search(sample_client, sample_address):
    search_str = sample_address.addressLine1 + ', ' + sample_address.postcode
    resp = sample_client.address_search(search_str)
    if STORE_RESULTS:
        result = [_.model_dump(mode='json') for _ in resp]
        results_file = Path('data/address_search_results.json')
        dump_result(result, results_file)

    assert isinstance(resp, list)
    assert isinstance(resp[0], AddressSummary)
    ...


# @pytest.mark.skip(reason='Use Cached')
def test_address_search_dps(sample_client, sample_address):
    addresses_payload = AddressFindDPSRequest(addresses=[sample_address])
    resp = sample_client.address_search_dps(addresses_payload)
    if STORE_RESULTS:
        result = [_.model_dump(mode='json') for _ in resp]
        results_file = Path('data/address_search_dps_results.json')
        dump_result(result, results_file)

    assert isinstance(resp, list)
    assert isinstance(resp[0], AddressFindDPSResponse)


# @pytest.mark.skip(reason='Use Cached result')
def test_address_get(sample_address_client, sample_address_id):
    resp = sample_address_client.get(sample_address_id)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/address_get_result.json')
        dump_result(result, results_file)
    assert isinstance(resp, AddressRecord)


# @pytest.mark.skip(reason='Use Cached result')
def test_handler_get_slots(sample_order_handler_client, sample_dps_results):
    dps = sample_dps_results.dps
    postcode = sample_dps_results.input.postcode.replace(' ', '')
    dps_postcode = postcode + dps
    item_count = 1
    resp = sample_order_handler_client.get_slots(dps_postcode, item_count)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/collection_order_handler_get_slots.json')
        dump_result(result, results_file)
    assert isinstance(resp, GetAvailableSlotsResponse)


@pytest.mark.skip(reason='NOT REGISTERED FOR PLAN DO WE EVEN NEED IT?')
def test_del_office(sample_del_office_client):
    postcode = 'NW6 4TE'
    resp = sample_del_office_client.get(postcode)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/delivery_office_finder_get_result.json')
        dump_result(result, results_file)
    assert 'searchedPostcode' in resp
    assert resp['header']['statusCode'] == '200'


def test_my_slot(sample_slots_response):
    send_date = date.today() + timedelta(days=3)
    myslot = sample_slots_response.match_date(send_date)
    assert isinstance(myslot, SlotDateDef)


def test_inbound_booking_story(
        sample_address,
        sample_client,
        sample_sender,
        sample_account_details,
):
    # get DPS
    dps_request = AddressFindDPSRequest(addresses=[sample_address])
    dps_responses = sample_client.address_search_dps(dps_request)
    dps_response = dps_responses[0]

    # get collection slot
    item_count = 1
    send_date = date.today() + timedelta(days=2)
    slots_response = sample_client.collection_slots_fetch(dps_response.dps_postcode, item_count)
    my_slot = slots_response.match_date(send_date)
    if my_slot is None:
        raise Exception('No slot found for date')
    token = slots_response.task_slots.slot_details.token_id
    ...
    dims = DimensionsPostDef(height=30, width=30, depth=30)
    item = ItemsPostDef(
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
        address=AddressNonMandatoryDef.model_validate(sample_address, from_attributes=True),
        collection_date=send_date,
        items=[item],
    )

    order_resp = sample_client.collection_create(collection_payload)
    ...


# def test_returns(sample_return_request, sample_return_client):
#     resp = sample_return_client.order_create_return(sample_return_request)
#     assert isinstance(resp, ReturnsResponse)
#     ...


def test_returns(sample_return_request, sample_client):
    resp = sample_client.order_create_return(sample_return_request)
    assert isinstance(resp, ReturnsResponse)
    ...


def test_fetch_orders(sample_client):
    res = sample_client.orders_fetch()
    assert isinstance(res, GetOrdersResponse)
    ...
