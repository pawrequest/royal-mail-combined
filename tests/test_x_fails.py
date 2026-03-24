def test_fails(fxt_client, fxt_order):
    order = fxt_order.model_copy(deep=True)
    order.postage_details.service_code = 'INVALID'
    # order.recipient.address.postcode = 'INVALID'  # force an error
    res = fxt_client.book_outbound_shipment(order)
    ...

