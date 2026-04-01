import contextlib
from collections.abc import Generator
from contextlib import AbstractContextManager
from pprint import pprint

from royal_mail_combined import RoyalMailClient
from royal_mail_combined.click_and_drop_api.models import GetOrdersResponse
from royal_mail_combined.config import RoyalMailSettingsGlobal


@contextlib.contextmanager
def temporary_client() -> AbstractContextManager[RoyalMailClient]:
    settings = RoyalMailSettingsGlobal.from_env()
    client = None
    orders_before = None
    try:
        client = RoyalMailClient(settings)
        orders_before: GetOrdersResponse = client.fetch_orders()
        pprint(orders_before.model_dump())
        yield client
    finally:
        if client and orders_before:
            orders_after: GetOrdersResponse = client.fetch_orders()
            for o in orders_after.orders:
                if o not in orders_before.orders:
                    print('Deleting Test Order')
                    res = client.cancel_outbound_shipment(order_identifiers=str(o.order_identifier))
                    assert o.order_identifier in res.order_idents(), 'WARNING, FAILED TO DELETE TEST ORDERS!!'
                    print('Deleted Test Orders')
