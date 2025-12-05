import json

import pytest

from royal_mail_combined.clients.address_client import AddressClient
from royal_mail_combined.clients.collection_order_client import CollectionOrderClient
from royal_mail_combined.clients.collection_order_handler_client import CollectionOrderHandlerClient
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
def sample_sender():
    return SenderDetailsPostDef(sender_name='Test Sender', sender_email='TestSender@Email.com')


@pytest.fixture(scope='session')
def sample_items():
    item = ItemsPostDef()


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