from royal_mail_combined import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal


def client():
    sets = RoyalMailSettingsGlobal.from_env()
    client_ = RoyalMailClient(settings=sets)
    return client_


def delete_all_orders():
    fxt_client = client()
    orders_after = fxt_client.fetch_orders().orders
    sure = input(
        f'This will delete the following orders, are you sure?\n{[_.order_identifier for _ in orders_after]}\n\n (y/n)'
    )
    if not sure.lower() == 'y':
        print('Aborting')
        return
    for o in orders_after.orders:
        res = fxt_client.cancel_outbound_shipment(order_identifiers=str(o.order_identifier))
        assert o.order_identifier in res.order_idents(), 'WARNING, FAILED TO DELETE TEST ORDERS!!'
        print('Deleted Order')


def cancel_collection(collection_id):
    fxt_client = client()
    res = fxt_client.parcel_api.cancel_collection(collection_id=collection_id)
    print(res)


if __name__ == '__main__':
    # delete_all_orders()
    c1 = 'CC-W307-135088399'
    c2 = 'CC-W307-135088435'
    cancel_collection(collection_id=c2)
