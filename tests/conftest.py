import pytest

from royal_mail_combined.clients.address import AddressClient
from royal_mail_combined.clients.collection_order_handler import CollectionOrderHandlerClient
from royal_mail_combined.clients.delivery_office_finder import DeliveryOfficeClient
from royal_mail_combined.config import RMSettings


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
def sample_del_office_client(sample_settings: RMSettings) -> DeliveryOfficeClient:
    return DeliveryOfficeClient(settings=sample_settings)

