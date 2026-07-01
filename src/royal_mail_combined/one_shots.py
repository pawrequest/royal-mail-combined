from pathlib import Path
from pprint import pprint

from royal_mail_combined import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.helpers import dump_result_model


def client():
    sets = RoyalMailSettingsGlobal.from_env()
    client_ = RoyalMailClient(settings=sets)
    return client_


def delete_order(order_id):
    fxt_client = client()
    res = fxt_client.cancel_outbound_shipment(order_identifiers=str(order_id))
    print(res)
    return res


def delete_all_orders():
    print('NOPE')
    return
    fxt_client = client()
    orders_after = fxt_client.fetch_orders().orders
    sure = input(
        f'This will delete the following orders, are you sure?\n{[_.order_identifier for _ in orders_after]}\n\n (y/n)'
    )
    if sure.lower() == 'y':
        for o in orders_after.orders:
            res = fxt_client.cancel_outbound_shipment(order_identifiers=str(o.order_identifier))
            assert o.order_identifier in res.order_idents(), 'WARNING, FAILED TO DELETE TEST ORDERS!!'
            print('Deleted Order')
    print('Aborting')
    return


def cancel_collection(collection_id):
    fxt_client = client()
    res = fxt_client.parcel_api.cancel_collection(collection_id=collection_id)
    print(res)


def get_collection(collection_id):
    fxt_client = client()
    res = fxt_client.parcel_api.collection_orders_api.order_get(collection_id)
    print(res)
    ...


def check_available_rtn_srvcs():
    fxt_client = client()
    res = fxt_client.http_client.check_return_services()
    pprint(res)
    dump_dir = r'C:\prdev\amdev\royal-mail-combined\tests'
    dump_result_model(res, Path(dump_dir))
    ...


if __name__ == '__main__':
    # delete_all_orders()
    # ident = '1326'
    # delete_order(ident)
    c1 = 'CC-W307-141687522'
    # get_collection(collection_id=c1)
    cancel_collection(collection_id=c1)
    # check_available_rtn_srvcs()
