BASE = r'https://api.royalmail.net'
ADDRESS_BASE = r'https://api.royalmail.net/addressfind/v1'
COLLECTION_HANDLER_BASE = BASE + r'/collectionorders/v1'
COLLECTION_SLOTS = COLLECTION_HANDLER_BASE + r'/slots'
SUBSCRIPTION_CHECK = COLLECTION_HANDLER_BASE + r'/productfamily/subscription'
DELIVERY_OFFICE_BASE = BASE + r'/deliveryOffices'

CAD_BASE = r'https://api.parcel.royalmail.com/api/v1'
CAD_ORDERS = CAD_BASE + r'/orders'
COLLECTION_ORDER = CAD_ORDERS + r'/v1/collectionOrder'
COLLECTION_ORDER_CREATE = COLLECTION_ORDER + r'/create'

RETURNS_ENDPOINT = CAD_BASE + r'/returns'
