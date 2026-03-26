from helpers import dump_result_model


def test_it(fxt_client, fxt_address):
    search_text = f'{fxt_address.postcode} {fxt_address.address_line1}'
    res = fxt_client.address_search(search_text)
    dump_result_model(res)
    ...


def test_retrieve(fxt_client):
    search = '80 East Avenue, Hayes, Middlesex'
    res = fxt_client.address_search(search)
    addr_id = res.addresses[0].address_id
    retrieved = fxt_client.address_retrieve(addr_id)
    dump_result_model(retrieved)
