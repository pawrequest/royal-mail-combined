import pytest


from royal_mail_combined.models.address import AddressRecord, AddressSummary


@pytest.mark.skip(reason="Use Cached result")
def test_address_search(sample_address_client):
    search_str = "amherst, 70 kingsgate road, london"
    resp = sample_address_client.search(search_str)
    assert isinstance(resp,list)
    assert isinstance(resp[0], AddressSummary)


def test_address_search_dps(sample_address_client):
    search_str = 'amherst, 70 kingsgate road, london'
    api_payload = {
        'Addresses': [
            {
                'addressLine1': '1 Elmgrove Rd',
                'addressLine2': 'Weybridge',
                'addressLine3': 'string',
                'postTown': 'Northamptonshire',
                'County': 'Northamptonshire',
                'postcode': 'NN15QS',
            },
        ]
    }
    # resp = sample_address_client.search_dps(search_str)
    resp = sample_address_client.search_dps(api_payload)
    assert isinstance(resp,list)
    assert isinstance(resp[0], AddressSummary)



@pytest.mark.skip(reason="Use Cached result")
def test_address_get(sample_address_client):
    address_id = "208117046094246242138076149120066080112124073194254111131026113007205065192248004075178194044026"
    resp = sample_address_client.get(address_id)
    assert isinstance(resp, AddressRecord)


def test_slots(sample_order_handler_client):
    resp = sample_order_handler_client.get_slots()
    ...


# def test_del_office(sample_del_office_client):
#     postcode = "SW1A 1AA"
#     resp = sample_del_office_client.get(postcode)
#     assert 'deliveryOffices' in resp

