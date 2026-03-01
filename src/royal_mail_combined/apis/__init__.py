from royal_mail_combined.apis.parcels_apis.address.api import AddressApi
from .click_and_drop.client import ClickAndDropClient
from .click_and_drop.api import LabelsApi, ManifestsApi, OrdersApi, VersionApi
from royal_mail_combined.apis.parcels_apis.collection_handler.api import GetAvailableSlotsApi, ProductFamilySubscriptionApi
from royal_mail_combined.apis.parcels_apis.collection_order.api import CollectionOrderApi, ReturnsCollectionApi

__all__ = [
    'AddressApi',
    'ClickAndDropClient',
    'LabelsApi',
    'ManifestsApi',
    'OrdersApi',
    'VersionApi',
    'GetAvailableSlotsApi',
    'ProductFamilySubscriptionApi',
    'CollectionOrderApi',
    'ReturnsCollectionApi'
]
