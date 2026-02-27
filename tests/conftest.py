import json

import pytest

from royal_mail_combined.click_and_drop.services import RoyalMailServiceCode, RoyalMailServiceCodeClickDrop
from royal_mail_combined.clients.address_client import AddressClient
from royal_mail_combined.clients.collection_order_client import CollectionOrderClient
from royal_mail_combined.clients.collection_order_handler_client import CollectionOrderHandlerClient
from royal_mail_combined.clients.returns_client import (
    Address,
    CustomerReference,
    ReturnsClient,
    ReturnsRequest,
    Service,
    Shipment,
)
from royal_mail_combined.delivery_office_finder.delivery_office_finder_client import DeliveryOfficeClient
from royal_mail_combined.config import RMSettings
from royal_mail_combined.address.address import AddressDef, AddressFindDPSResponse
from royal_mail_combined.collection_order.collection_order import AccountDetailsDef, ItemsPostDef, SenderDetailsPostDef
from royal_mail_combined.collection_order.collection_order_handler import GetAvailableSlotsResponse


@pytest.fixture(scope='session')
def sample_settings() -> RMSettings:
    return RMSettings.from_env()


@pytest.fixture(scope='session')
def sample_address_client(sample_settings: RMSettings) -> AddressClient:
    return AddressClient(settings=sample_settings)


@pytest.fixture(scope='session')
def sample_order_handler_client(sample_settings: RMSettings) -> CollectionOrderHandlerClient:
    return CollectionOrderHandlerClient(settings=sample_settings)


@pytest.fixture(scope='session')
def sample_order_client(sample_settings: RMSettings) -> CollectionOrderClient:
    return CollectionOrderClient(settings=sample_settings)


@pytest.fixture(scope='session')
def sample_del_office_client(sample_settings: RMSettings) -> DeliveryOfficeClient:
    return DeliveryOfficeClient(settings=sample_settings)


@pytest.fixture(scope='session')
def sample_address() -> AddressDef:
    return AddressDef(
        addressLine1='Flat 43, Berberis House',
        addressLine2='Highfield Road',
        postTown='Feltham',
        County='Middlesex',
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


# @pytest.fixture(scope='session')
# def sample_items():
#     item = ItemsPostDef()


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
def sample_return_client(sample_settings: RMSettings) -> ReturnsClient:
    return ReturnsClient(settings=sample_settings)


@pytest.fixture(scope='session')
def sample_return_request(sample_address, sample_sender, sample_return_address):
    ship_add = Address(
        title='Mr',
        first_name='ShipFirst',
        last_name='ShipLast',
        company_name='ShipCompany',
        address_line_1=sample_address.addressLine1,
        address_line_2=sample_address.addressLine2,
        address_line_3=sample_address.addressLine3,
        city=sample_address.postTown,
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
        address_line_1=sample_return_address.addressLine1,
        address_line_2=sample_return_address.addressLine2,
        address_line_3=sample_return_address.addressLine3,
        city=sample_return_address.postTown,
        county=sample_return_address.county,
        postcode=sample_return_address.postcode,
        country='United Kingdom',
        country_iso_code='GBR',
    )
    cust_ref = CustomerReference(reference='RETURN123456')
    service = Service(service_code=RoyalMailServiceCodeClickDrop.EXPRESS_24_RETURN)
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
