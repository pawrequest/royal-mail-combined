from royal_mail_combined.clients._base_client import _RMBaseClient

COLLECTION_HANDLER_BASE = r'https://api.royalmail.net/collectionorders/v1'


class CollectionOrderHandlerClient(_RMBaseClient):
    def get_slots(self, dps: str, item_count: int):
        params = {'dps': dps, 'itemCount': item_count}
        resp = self._do_get(url=f'{COLLECTION_HANDLER_BASE}/slots', params=params).json()
        return resp

    # def subscribe(self, ):