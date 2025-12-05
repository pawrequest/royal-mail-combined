from royal_mail_combined.clients._base_client import _RMBaseClient
from royal_mail_combined.collection_order.collection_order_handler import GetAvailableSlotsResponse

COLLECTION_HANDLER_BASE = r'https://api.royalmail.net/collectionorders/v1'


class CollectionOrderHandlerClient(_RMBaseClient):
    def get_slots(self, dps: str, item_count: int | str) -> GetAvailableSlotsResponse:
        params = {'dps': dps, 'itemCount': item_count}
        resp = self._do_get(url=f'{COLLECTION_HANDLER_BASE}/slots', params=params).json()
        slots = GetAvailableSlotsResponse(**resp)
        return slots

