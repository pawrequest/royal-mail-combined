import pytest

from conftest import STORE_RESULTS, TEST_DATE, dump_result_model
from royal_mail_combined.all_models import (
    ReturnsResponse,
)


def test_book_outbound(fxt_client, fxt_order):
    dump_result_model(fxt_order)
    res = fxt_client.click_and_drop.book_shipment(fxt_order)
    dump_result_model(res)
    ident = str(res.created_orders[0].order_identifier)
    fetched = fxt_client.fetch_specific_orders(order_identifiers=ident)
    assert str(fetched[0].order_identifier) == ident
    ...


def test_book_inbound(fxt_return_req, fxt_client):
    resp = fxt_client.book_inbound_shipment(fxt_return_req)
    if STORE_RESULTS:
        dump_result_model(resp)
    assert isinstance(resp, list) and all(isinstance(item, ReturnsResponse) for item in resp)


def test_book_inbound_with_collection_cancel_collection(fxt_client, fxt_return_req):
    res = fxt_client.book_inbound_shipment_with_collection(fxt_return_req, TEST_DATE, 2)
    dump_result_model(res)
    assert res.status == 'Order created successfully'
    collect_id = res.collection_order_id

    res = fxt_client.parcel_api.cancel_collection(collect_id)
    dump_result_model(res)
    assert res.status == 'Order cancelled successfully'


BOOKEDIDS = []


@pytest.mark.skip(reason='Need real collection ids to test cancellation')
def test_cancel_collection(fxt_client):
    res = fxt_client.parcel_api.cancel_collection(BOOKEDIDS[1])
    dump_result_model(res)
    assert res.status == 'Order cancelled successfully'
    ...
