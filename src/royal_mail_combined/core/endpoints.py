from __future__ import annotations

BASE_NET = r'https://api.royalmail.net'
ADDRESS_BASE = r'https://api.royalmail.net/addressfind/v1'
ORDERS_NET = r'https://api.royalmail.net/orders/v1'
COLLECTION_HANDLER_NET = BASE_NET + r'/collectionorders/v1'
COLLECTION_SLOTS = COLLECTION_HANDLER_NET + r'/slots'
SUBSCRIPTION_CHECK = COLLECTION_HANDLER_NET + r'/productfamily/subscription'
DELIVERY_OFFICE_BASE = BASE_NET + r'/deliveryOffices'

CAD_BASE = r'https://api.parcel.royalmail.com/api/v1'
CAD_ORDERS = CAD_BASE + r'/orders'
CAD_COLLECTION_ORDER = CAD_ORDERS + r'/v1/collectionOrder'
COLLECTION_ORDER_CREATE = CAD_COLLECTION_ORDER + r'/create'

RETURNS_ENDPOINT = CAD_BASE + r'/returns'
RETURNS_SERVICES_ENDPOINT = RETURNS_ENDPOINT + r'/services'
TRACKING_LINK_BASE = r'https://www.royalmail.com/track-your-item#/tracking-results'


def tracking_link(tracking_number: str) -> str:
    return f'{TRACKING_LINK_BASE}/{tracking_number}'
