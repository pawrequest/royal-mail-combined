from royal_mail_combined.apis.parcels_apis.address.models import AddressesDef
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
    res = sample_client.address_search('30 bennet close')
    assert isinstance(res, AddressesDef)
    ...

