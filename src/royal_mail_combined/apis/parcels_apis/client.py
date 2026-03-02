from royal_mail_combined.apis import AddressApi, CollectionOrderApi, GetAvailableSlotsApi, ProductFamilySubscriptionApi
from royal_mail_combined.apis.parcels_apis.address.models import AddressFindRequestDef
from royal_mail_combined.apis.parcels_apis.collection_handler.models import (ProductFamily, ProductFamilyDef)
from royal_mail_combined.build_client import build_client
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.endpoints import (
    ADDRESS_BASE,
    COLLECTION_HANDLER_NET,
    CAD_COLLECTION_ORDER,
    CAD_ORDERS,
    ORDERS_NET,
)


class ParcelAPIClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        self.settings = settings
        # address_client = ApiClient(configuration=settings.api_config(ADDRESS_BASE))
        address_client = build_client(settings, host=ADDRESS_BASE)
        self.address_api = AddressApi(address_client)
        self.address_retrieve = self.address_api.address_retrieve
        self.address_verify = self.address_api.address_verify

        # collection_client = ApiClient(configuration=settings.api_config(COLLECTION_ORDER))
        collection_client = build_client(settings, host=ORDERS_NET)
        self.collection_orders_api = CollectionOrderApi(collection_client)
        self.collection_create = self.collection_orders_api.order_create
        self.collection_create_mandatory = self.collection_orders_api.order_create_mandatory

        collection_handler_client = build_client(settings, host=COLLECTION_HANDLER_NET)
        self.slots_api = GetAvailableSlotsApi(collection_handler_client)
        self.slots_get_available = self.slots_api.order_get_available_slots
        self.subs_api = ProductFamilySubscriptionApi(collection_handler_client)

    def address_search(self, address_text: str):
        req = AddressFindRequestDef(address_text=address_text)
        return self.address_api.address_find(address_find_request=req)

    def collection_subscription_check(self, barcode, family_name, account_number):
        pf_ = ProductFamilyDef(account_number=account_number, barcode=barcode, product_family_name=family_name)
        pf = ProductFamily(product_family=[pf_])
        res = self.subs_api.order_validate_subscription(product_family=pf)
        return res
