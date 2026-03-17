from royal_mail_combined import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal


def client():
    sets = RoyalMailSettingsGlobal.from_env()
    client_ = RoyalMailClient(settings=sets)
    return client_


def delete_all_orders():
    sure = input('This will delete ALL ORDERS in the account, are you sure? (y/n)')
    fxt_client = client()
    if sure.lower() == 'y':
        orders_after = fxt_client.fetch_orders()
        for o in orders_after.orders:
            res = fxt_client.cancel_outbound_shipment(order_identifiers=str(o.order_identifier))
            assert o.order_identifier in res.order_idents(), 'WARNING, FAILED TO DELETE TEST ORDERS!!'
            print('Deleted Order')


# if __name__ == "__main__":
#     delete_all_orders()
