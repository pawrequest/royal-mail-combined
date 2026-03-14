from conftest import STORE_RESULTS, dump_result_model, print_object
from royal_mail_combined.all_models import (
    AddressRecordDef,
    AddressVerifyDef,
    AddressVerifyReqRespdef,
    AddressVerifyRequestDef,
    AddressesDef,
    GetOrdersResponse,
    GetVersionResource,
)
from royal_mail_combined.click_and_drop_api.models import GetOrderInfoResource


def test_version(fxt_client):
    res = fxt_client.click_and_drop.version_api.get_version_async()
    assert isinstance(res, GetVersionResource)
    ...


def test_get_orders(fxt_client):
    res = fxt_client.fetch_orders()
    assert isinstance(res, GetOrdersResponse)
    print_object(res)
    ...


def test_addresses(fxt_client):
    res = fxt_client.address_search("30 bennet close")
    assert isinstance(res, AddressesDef)
    print_object(res)
    ...


# @pytest.mark.skip(reason='unable to cancel?')


def test_return_services(fxt_client):
    res = fxt_client.http_client.check_return_services()
    if STORE_RESULTS:
        dump_result_model(res)
    ...


def test_fetch_orders(fxt_client):
    res = fxt_client.fetch_orders()
    if STORE_RESULTS:
        dump_result_model(res)
    assert isinstance(res, GetOrdersResponse)
    ...


def test_fetch_specific(fxt_client):
    track2 = "PK007810419GB"
    a_real_shipment_id = 1037
    tracking_number = "ZS191785051GB"
    unique_item_id = "32073580900070C28FE67"
    # idents = quote(tracking_number)
    # idents = quote(f'"{tracking_number}";"{unique_item_id}"')
    # idents = f'"{quote(unique_item_id)}"'

    office_res_unique = r"32073580900070CE96492"
    office_res_track = r"ZS191785065GB"

    identifier = str(a_real_shipment_id)
    # identifier = order_identifier_to_string(office_res_track)

    res = fxt_client.fetch_specific_orders(order_identifiers=identifier)
    assert isinstance(res[0], GetOrderInfoResource)
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


def test_address_search(fxt_client, fxt_address):
    search_str = fxt_address.address_line1 + ", " + fxt_address.postcode
    resp: AddressesDef = fxt_client.parcel_api.address_search(search_str)
    if STORE_RESULTS:
        dump_result_model(resp)

    assert isinstance(resp, AddressesDef)
    ...


def test_address_search_dps(fxt_client, fxt_address):
    addr = AddressVerifyDef.model_validate(fxt_address, from_attributes=True)
    addresses_payload = AddressVerifyRequestDef(addresses=[addr])
    resp: list[AddressVerifyReqRespdef] = fxt_client.address_verify(addresses_payload)
    if STORE_RESULTS:
        dump_result_model(resp)
    assert isinstance(resp, list)
    assert isinstance(resp[0], AddressVerifyReqRespdef)


def test_address_get(fxt_client, cached_address_id):
    resp = fxt_client.address_retrieve(cached_address_id)
    if STORE_RESULTS:
        dump_result_model(resp)
    assert isinstance(resp, AddressRecordDef)


# todo fixme
# def test_handler_get_slots(fxt_client):
#
#     dps = cached_dps_results.dps
#     postcode = cached_dps_results.input.postcode.replace(' ', '')
#     dps_postcode_str = postcode + dps
#     item_count = 1
#     resp = fxt_client.parcel_api.slots_api.order_get_available_slots(dps_postcode_str, item_count)
#     if STORE_RESULTS:
#         dump_result_model(resp)
#     assert isinstance(resp, GetAvailableSlotsResponse)
