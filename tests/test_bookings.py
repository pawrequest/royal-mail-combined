from pathlib import Path

import pytest
from loguru import logger

from conftest import STORE_RESULTS, TEST_DATE, dump_result_model

from royal_mail_combined.click_and_drop_api.models.return_models import ReturnResponseContainer
from royal_mail_combined.core.consts_types import ResponseMessages
from pawdf.array_pdf.array_p import on_a4


def write_label_file(label_content: bytes, label_path: Path):
    unsize = label_path.parent / "original_size" / label_path.name
    unsize.parent.mkdir(parents=True, exist_ok=True)
    unsize.write_bytes(label_content)
    logger.info(f"Resizing {unsize} to A4 at {label_path}")
    on_a4(input_file=unsize, output_file=label_path)
    logger.info(f"Wrote label to {label_path}")


def test_book_outbound(fxt_client, fxt_order):
    dump_result_model(fxt_order)
    res = fxt_client.book_outbound_shipment(fxt_order)
    dump_result_model(res)
    ident = str(res.created_orders[0].order_identifier)
    idents_multi = res.success_idents
    fetched_multi = fxt_client.fetch_specific_orders(order_identifiers=idents_multi)
    labels = fxt_client.get_label_data(order_identifiers=idents_multi)
    write_label_file(labels, Path(f"labels/{ident}.pdf"))

    fetched = fxt_client.fetch_specific_orders(order_identifiers=ident)
    assert str(fetched[0].order_identifier) == ident
    assert (
        str(sorted(fetched_multi, key=lambda v: v.order_identifier)[0].order_identifier)
        == sorted(res.success_idents.split(";"))[0]
    )
    ...


def test_book_inbound(fxt_return_request_container, fxt_client):
    resp = fxt_client.book_inbound_shipment(fxt_return_request_container)
    if STORE_RESULTS:
        dump_result_model(resp)
    assert isinstance(resp, ReturnResponseContainer)


def test_book_inbound_with_collection_cancel_collection(fxt_client, fxt_return_request_container):
    res = fxt_client.book_inbound_shipment_with_collection(fxt_return_request_container, TEST_DATE)
    dump_result_model(res)
    assert res.collection_response.status == ResponseMessages.COLLECTION_CREATED
    collect_id = res.collection_response.collection_order_id

    res = fxt_client.parcel_api.cancel_collection(collect_id)
    dump_result_model(res)
    assert res.status == ResponseMessages.COLLECTION_CANCELLED


BOOKEDIDS = []


@pytest.mark.skip(reason="Need real collection ids to test cancellation")
def test_cancel_collection(fxt_client):
    res = fxt_client.parcel_api.cancel_collection(BOOKEDIDS[1])
    dump_result_model(res)
    assert res.status == ResponseMessages.COLLECTION_CANCELLED
    ...
