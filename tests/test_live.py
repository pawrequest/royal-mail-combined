from pathlib import Path

import pytest

from royal_mail_combined.apis.parcels_apis.collection_handler.models import GetAvailableSlotsResponse
from royal_mail_combined.apis.parcels_apis.collection_order.models import (
    Collection,
    CollectionItemType,
    DimensionsPostDef,
    ItemsPostDef, AddressNonMandatoryDef,
)
from royal_mail_combined.apis.returns.models import ReturnsResponse
from royal_mail_combined.converters import (
    addr_mandatory,
    addr_non_mandatory_from_addr,
    dps_postcode,
    match_date,
    rtn_address_to_addr_verify,
)
from conftest import (STORE_RESULTS, TEST_DATE, cached_order, dump_result, dump_result_model)


# @pytest.mark.skip(
#     reason='This is a live test, it will create an order in the account, check online portal to confirm deletion after test'
# )
def test_make_booking(sample_client, cached_order):
    res = sample_client.click_and_drop.book_shipment(cached_order)
    dump_result_model(res)
    ident = str(res.created_orders[0].order_identifier)
    fetched = sample_client.click_and_drop.fetch_specific(order_identifiers=ident)
    assert str(fetched[0].order_identifier) == ident
    ...


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


@pytest.mark.skip(reason='unable to cancel?')
def test_returns(cached_return_request, sample_client):
    resp = sample_client.create_return_shipment_order(cached_return_request)
    if STORE_RESULTS:
        dump_result_model(resp)
    assert isinstance(resp, ReturnsResponse)
    ...


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

    res = sample_client.click_and_drop.fetch_specific(order_identifiers=idents)
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


@pytest.mark.skip(reason='Use Cached result')
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


def test_inbound_booking_story(
        cached_address_verify,
        sample_client,
        cached_sender,
        cached_account_details,
        cached_return_response,
        cached_return_request,
        cached_return_services
):
    # get DPS
    collection_address_verify = rtn_address_to_addr_verify(cached_return_request.shipment.shipping_address)
    dps_request = AddressVerifyRequestDef(addresses=[collection_address_verify])
    dps_responses = sample_client.parcel_api.address_verify(dps_request)
    dump_result_model(dps_responses)

    addr_verify_reqresp = dps_responses[0]
    dps_pc = dps_postcode(addr_verify_reqresp)

    # get collection slot
    item_count = 1
    slots_response = sample_client.parcel_api.slots_get_available(
        dps=dps_pc,
        item_count=item_count
    )
    dump_result_model(slots_response)
    my_slot = match_date(slots_response, TEST_DATE)
    if my_slot is None:
        raise Exception('No slot found for date')
    token = slots_response.task_slots.slot_details.token_id
    ...

    serv = cached_return_services.lookup_service_by_code(cached_return_request.service.service_code)
    barcode_id = cached_return_response.shipment.tracking_number
    dims = DimensionsPostDef(height=30, width=30, depth=30)
    item = ItemsPostDef(
        item_barcode_id=barcode_id,
        weight_in_grams=10000,
        item_service_name=serv.service_name,
        item_type=CollectionItemType.STANDARD,
        dimensions=dims,
    )

    # book collection
    collection_address_mand = addr_mandatory(collection_address_verify, dps=addr_verify_reqresp.dps)
    collection_address_non = AddressNonMandatoryDef(
        **collection_address_verify.model_dump(), dps=addr_verify_reqresp.dps,
    )
    collection = Collection(
        timeslot_reservation_id=token,
        sender_details=cached_sender,
        account_details=cached_account_details,
        address=collection_address_non,
        collection_date=TEST_DATE,
        items=[item],
    )

    dump_result_model(collection)
    order_resp = sample_client.parcel_api.collection_create(collection=collection)
    ...
    # order_resp = sample_client.parcel_api.collection_create_mandatory(collection=collection_mandatory)
    # collection = Collection(
    #     timeslot_reservation_id=token,
    #     sender_details=cached_sender,
    #     account_details=cached_account_details,
    #     address=addr_non_mandatory_from_addr(cached_address_verify),
    #     collection_date=TEST_DATE,
    #     items=[item],
    # )
    # dump_result_model(collection_payload)
    # order_resp = sample_client.parcel_api.collection_create(collection=collection_payload)
    ...

    # order_resp = sample_client.parcel_api.collection_create(collection=collection_payload)
