import json
from pprint import pprint
from typing import Any, Generator

import pytest

from royal_mail_combined.added_models.services import RoyalMailServiceCodes
from royal_mail_combined.apis.click_and_drop.models import GetOrdersResponse
from royal_mail_combined.apis.parcels_apis.address.models import AddressVerifyDef
from royal_mail_combined.apis.parcels_apis.collection_handler.models import GetAvailableSlotsResponse
from royal_mail_combined.apis.parcels_apis.address.added_models import AddressFindDPSResponse
from royal_mail_combined.apis.parcels_apis.collection_order.models import AddressDef, SenderDetailsPostDef, AccountDetailsDef
from royal_mail_combined.apis.returns.models import (
    ReturnsRequest,
    Service, Address, CustomerReference, Shipment,
)
from royal_mail_combined.client_multi import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal


@pytest.fixture(scope='session')
def sample_settings() -> RoyalMailSettingsGlobal:
    return RoyalMailSettingsGlobal.from_env()


@pytest.fixture(scope='session')
def sample_client(sample_settings) -> Generator[RoyalMailClient, Any, None]:
    """Test client - automatically removes orders created during testing on completion"""
    client = RoyalMailClient(sample_settings)
    orders_before: GetOrdersResponse = client.click_and_drop.fetch_orders()
    pprint(orders_before.model_dump())

    yield client

    print('Deleting Test Orders')
    orders_after: GetOrdersResponse = client.click_and_drop.fetch_orders()
    for o in orders_after.orders:
        if o not in orders_before.orders:
            res = client.click_and_drop.delete_orders(order_identifiers=o.order_identifier)
            assert o.order_identifier in res.idents, 'WARNING, FAILED TO DELETE TEST ORDERS!!'
            print('Deleted Test Orders')


@pytest.fixture(scope='session')
def sample_address() -> AddressDef:
    return AddressDef(
        addressLine1='Flat 43, Berberis House',
        addressLine2='Highfield Road',
        postTown='Feltham',
        County='Middlesex', #  mixed pascal and camel in rm api.
        postcode='TW13 4GP',
    )


@pytest.fixture(scope='session')
def sample_address_verify() -> AddressVerifyDef:
    return AddressVerifyDef(
        addressLine1='Flat 43, Berberis House',
        addressLine2='Highfield Road',
        postTown='Feltham',
        County='Middlesex', #  mixed pascal and camel in rm api.
        postcode='TW13 4GP',
    )


@pytest.fixture(scope='session')
def sample_return_address():
    return AddressDef(
        addressLine1='70 Kingsgate Road',
        postTown='Kilburn',
        County='London',
        postcode='NW64TE',
    )


@pytest.fixture(scope='session')
def sample_sender():
    return SenderDetailsPostDef(sender_name='Test Sender', sender_email='TestSender@Email.com')


@pytest.fixture(scope='session')
def sample_account_details(sample_settings):
    return AccountDetailsDef(retailer_account_number=sample_settings.account_number)


@pytest.fixture(scope='session')
def sample_slots_response():
    with open(r'data\collection_order_handler_get_slots.json', 'r') as f:
        res = f.read()
    return GetAvailableSlotsResponse.model_validate_json(res)


@pytest.fixture(scope='session')
def sample_address_id():
    return '068077252071149193225174041225027138078204116070010065014066078136091212102005045066044184012023'


@pytest.fixture(scope='session')
def sample_dps_results() -> AddressFindDPSResponse:
    with open(r'data\address_search_dps_results.json', 'r') as f:
        res = f.read()
        res = json.loads(res)
    return AddressFindDPSResponse.model_validate(res[0])


@pytest.fixture(scope='session')
def sample_return_request(sample_address, sample_sender, sample_return_address):
    ship_add = Address(
        title='Mr',
        first_name='ShipFirst',
        last_name='ShipLast',
        company_name='ShipCompany',
        address_line_1=sample_address.address_line1,
        address_line_2=sample_address.address_line2,
        address_line_3=sample_address.address_line3,
        city=sample_address.post_town,
        county=sample_address.county,
        postcode=sample_address.postcode,
        country='United Kingdom',
        country_iso_code='GBR',
    )
    return_add = Address(
        title='Mr',
        first_name='ReturnFirst',
        last_name='ReturnLast',
        company_name='ReturnCompany',
        address_line_1=sample_return_address.address_line1,
        address_line_2=sample_return_address.address_line2,
        address_line_3=sample_return_address.address_line3,
        city=sample_return_address.post_town,
        county=sample_return_address.county,
        postcode=sample_return_address.postcode,
        country='United Kingdom',
        country_iso_code='GBR',
    )
    cust_ref = CustomerReference(reference='RETURN123456')
    service = Service(service_code=RoyalMailServiceCodes.TRACKED_24_RTN)
    shipment = Shipment(
        shipping_address=ship_add,
        return_address=return_add,
        customer_reference=cust_ref,
    )
    return ReturnsRequest(
        service=service,
        shipment=shipment,
    )


@pytest.fixture(scope='session')
def sample_return_request_json_example():
    return {
        'service': {'serviceCode': 'TSS'},
        'shipment': {
            'shippingAddress': {
                'title': 'Mr',
                'firstName': 'Name',
                'lastName': 'Surname',
                'companyName': 'Company LTD',
                'addressLine1': '23 fish lane',
                'addressLine2': '',
                'addressLine3': '',
                'city': 'Milton Keynes',
                'county': '',
                'postcode': 'MK17 8EW',
                'country': 'United kingdom',
                'countryIsoCode': 'GBR',
            },
            'returnAddress': {
                'title': 'string',
                'firstName': 'string',
                'lastName': 'string',
                'companyName': 'string',
                'addressLine1': '15 clown lane',
                'addressLine2': 'string',
                'addressLine3': 'string',
                'city': 'string',
                'county': 'string',
                'postcode': 'MK17 8EW',
                'country': 'united kingdom',
                'countryIsoCode': 'GBR',
            },
            'customerReference': {'reference': 'Testing Reference'},
        },
    }


@pytest.fixture(scope='session')
def sample_return_request_json():
    return {
        'service': {'serviceCode': 'RT0'},
        'shipment': {
            'shippingAddress': {
                'title': 'Mr',
                'firstName': 'Name',
                'lastName': 'Surname',
                'companyName': 'Company LTD',
                'addressLine1': '30 Bennet Close',
                'addressLine2': '',
                'addressLine3': '',
                'city': 'Welling',
                'county': 'Kent',
                'postcode': 'DA16 3HU',
                'country': 'United kingdom',
                'countryIsoCode': 'GBR',
            },
            'returnAddress': {
                'title': 'Mr',
                'firstName': 'Giles',
                'lastName': 'Toman',
                'companyName': 'Amherst Enterprises',
                'addressLine1': '70 Kingsgate Road',
                'addressLine2': '',
                'addressLine3': '',
                'city': 'Kilburn',
                'county': 'London',
                'postcode': 'NW64TE',
                'country': 'United Kingdom',
                'countryIsoCode': 'GBR',
            },
            'customerReference': {'reference': 'Testing Reference'},
        },
    }
