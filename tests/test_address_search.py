from helpers import dump_result_model


def test_it(fxt_client, fxt_address):
    search_text = f'{fxt_address.postcode} {fxt_address.address_line1}'
    res = fxt_client.address_search(search_text)
    dump_result_model(res)
    ...
