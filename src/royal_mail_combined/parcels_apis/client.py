from datetime import date

from royal_mail_combined.all_models import AddressFindRequestDef, ProductFamily, ProductFamilyDef
from royal_mail_combined.converters import match_collection_slot_date
from royal_mail_combined.parcels_apis.address.api import AddressApi
from royal_mail_combined.parcels_apis.collection_order.api import CollectionOrderApi
from royal_mail_combined.parcels_apis.collection_handler.api import GetAvailableSlotsApi, ProductFamilySubscriptionApi
from royal_mail_combined.core.build_client import build_client
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.endpoints import (
    ADDRESS_BASE,
    COLLECTION_HANDLER_NET,
    ORDERS_NET,
)
from royal_mail_combined.parcels_apis.collection_order.models import CollectionStatus, CollectionStatusRequestDef


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

    def cancel_collection(self, collection_id: str):
        req = CollectionStatusRequestDef(status=CollectionStatus.CANCELLED)
        return self.collection_orders_api.order_delete(collection_id=collection_id, collection_status_request=req)

    def get_token(self, collection_date: date, num_boxes: int, postcode_and_dps: str) -> str | None:
        slots_response = self.slots_get_available(dps=postcode_and_dps, item_count=num_boxes)
        my_slot = match_collection_slot_date(slots_response, collection_date)
        if my_slot is None:
            raise Exception('No slot found for date')
        token = slots_response.task_slots.slot_details.token_id
        return token
