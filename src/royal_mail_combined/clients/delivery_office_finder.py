from royal_mail_combined.clients._base_client import _RMBaseClient


class DeliveryOfficeClient(_RMBaseClient):
    def get(self, postcode: str):
        delivery_office_url = r'https://api.royalmail.net/deliveryOffices'
        params = {'postcode': postcode}
        return self._do_get(url=delivery_office_url, params=params).json()