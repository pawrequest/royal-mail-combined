from pathlib import Path

import pytest

from royal_mail_combined.apis.parcels_apis.collection_handler.models import GetAvailableSlotsResponse
from royal_mail_combined.converters import (
    order_identifier_to_string,
)
from conftest import (STORE_RESULTS, dump_result, dump_result_model)


# @pytest.mark.skip(
#     reason='This is a live test, it will create an order in the account, check online portal to confirm deletion after test'
# )


from royal_mail_combined.apis.parcels_apis.address.models import (
    AddressesDef,
    AddressVerifyDef,
    AddressVerifyRequestDef,
    AddressVerifyReqRespdef, AddressRecordDef,
)
from royal_mail_combined.apis.click_and_drop.models import GetOrdersResponse, GetVersionResource


def test_version(sample_client):
    res = sample_client.click_and_drop.fetch_version()
    assert isinstance(res, GetVersionResource)
    ...


def test_get_orders(sample_client):
    res = sample_client.click_and_drop.fetch_orders()
    assert isinstance(res, GetOrdersResponse)
    ...


def test_addresses(sample_client):
    res = sample_client.parcel_api.address_search('30 bennet close')
    assert isinstance(res, AddressesDef)
    ...


# @pytest.mark.skip(reason='unable to cancel?')


def test_return_services(sample_client):
    res = sample_client.check_return_services()
    if STORE_RESULTS:
        dump_result_model(res)
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
    track2 = 'PK007810419GB'
    anitem = 1038
    tracking_number = "ZS191785051GB"
    unique_item_id = "32073580900070C28FE67"
    # idents = quote(tracking_number)
    # idents = quote(f'"{tracking_number}";"{unique_item_id}"')
    # idents = f'"{quote(unique_item_id)}"'
    idents = str(anitem)

    office_res_unique = r'32073580900070CE96492'
    office_res_track = r'ZS191785065GB'

    identifier = order_identifier_to_string(office_res_track)

    res = sample_client.click_and_drop.fetch_specific(order_identifiers=identifier)
    if STORE_RESULTS:
        dump_result_model(res)
    ...
    # ident = '32073580900070AD6B7F8' # uniquesItemId from returns endpoint
    # sample_client.label_data_fetch(order_idents=ident)
    ...

    # book return
    # fetch order info
    # use info to book collection
    # cancel collection
    ...


# @pytest.mark.skip(reason='Use Cached result')
def test_address_search(sample_client, cached_address):
    search_str = cached_address.address_line1 + ', ' + cached_address.postcode
    resp: AddressesDef = sample_client.parcel_api.address_search(search_str)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/address_search_results.json')
        dump_result(result, results_file)

    assert isinstance(resp, AddressesDef)
    ...


@pytest.mark.skip(reason='Use Cached')
def test_address_search_dps(sample_client, cached_address):
    addr = AddressVerifyDef.model_validate(cached_address, from_attributes=True)
    addresses_payload = AddressVerifyRequestDef(addresses=[addr])
    resp: list[AddressVerifyReqRespdef] = sample_client.address_search_verify(addresses_payload)
    if STORE_RESULTS:
        result = [_.model_dump(mode='json') for _ in resp]
        results_file = Path('data/address_search_dps_results.json')
        dump_result(result, results_file)

    assert isinstance(resp, list)
    assert isinstance(resp[0], AddressVerifyReqRespdef)


@pytest.mark.skip(reason='Use Cached result')
def test_address_get(sample_client, cached_address_id):
    resp = sample_client.address_fetch(cached_address_id)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/address_get_result.json')
        dump_result(result, results_file)
    assert isinstance(resp, AddressRecordDef)


@pytest.mark.skip(reason='Use Cached result')
def test_handler_get_slots(sample_client, cached_dps_results):
    dps = cached_dps_results.dps
    postcode = cached_dps_results.input.postcode.replace(' ', '')
    dps_postcode_str = postcode + dps
    item_count = 1
    resp = sample_client.parcel_api.slots_get_available(dps_postcode_str, item_count)
    if STORE_RESULTS:
        result = resp.model_dump(mode='json')
        results_file = Path('data/collection_order_handler_get_slots.json')
        dump_result(result, results_file)
    assert isinstance(resp, GetAvailableSlotsResponse)


