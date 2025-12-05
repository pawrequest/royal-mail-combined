from royal_mail_combined.clients._base_client import _RMBaseClient
from royal_mail_combined.collection_order.collection_order import Collection

CREATE_URL = r'https://api.royalmail.net/orders/v1/collectionOrder/create'


class CollectionOrderClient(_RMBaseClient):
    def create_order(self, data: Collection):
        resp = self._do_post(url=CREATE_URL, data=data)
        return resp

