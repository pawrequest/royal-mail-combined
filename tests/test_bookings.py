import pytest

from conftest import REFERENCE, STORE_RESULTS, TEST_DATE, dump_result_model
from royal_mail_combined.added_models.services import RoyalMailServiceCodes
from royal_mail_combined.apis.parcels_apis.address.models import AddressVerifyRequestDef
from royal_mail_combined.apis.parcels_apis.collection_order.models import (
    AccountDetailsDef, AddressMandatoryDef, AddressNonMandatoryDef, Collection, CollectionItemType,
    CollectionMandatory, DimensionsPostDef,
    ItemsPostDef, SenderDetailsPostDef,
)
from royal_mail_combined.apis.returns.models import (
    Address,
    CustomerReference,
    ReturnsRequest,
    ReturnsResponse,
    Service,
    Shipment,
)
from royal_mail_combined.converters import (
    addr_mandatory_f_addr_and_dps,
    address_angonstic_to_verify_def,
    match_date,
    rtn_address_to_addr_verify,
)


def test_make_booking(sample_client, cached_order):
    res = sample_client.click_and_drop.book_shipment(cached_order)
    dump_result_model(res)
    ident = str(res.created_orders[0].order_identifier)
    fetched = sample_client.click_and_drop.fetch_specific(order_identifiers=ident)
    assert str(fetched[0].order_identifier) == ident
    ...


@pytest.fixture(scope='session')
def return_request():
    sender_address = Address(
        title='Mr',
        first_name='ShipFirst',
        last_name='ShipLast',
        company_name='ShipCompany',
        address_line1='Flat 43, Berberis House',
        address_line2='Highfield Road',
        city='Feltham',
        county='Middlesex',  # mixed pascal and camel in rm api.
        postcode='TW13 4GP',
        country='United Kingdom',
        country_iso_code='GBR',
    )
    destination_address = Address(
        title='Mr',
        first_name='ReturnFirst',
        last_name='ReturnLast',
        company_name='ReturnCompany',
        address_line1='70 Kingsgate road',
        city='Kilburn',
        county='London',
        postcode='NW6 4TE',
        country='United Kingdom',
        country_iso_code='GBR',
    )

    cust_ref = CustomerReference(reference=REFERENCE)
    service = Service(service_code=RoyalMailServiceCodes.TRACKED_24_RTN)
    shipment = Shipment(
        shipping_address=destination_address,
        return_address=sender_address,
        customer_reference=cust_ref,
    )
    return ReturnsRequest(
        service=service,
        shipment=shipment,
    )


def test_make_booking_return(return_request, sample_client):
    resp = sample_client.create_return_shipment_order(return_request)
    if STORE_RESULTS:
        dump_result_model(resp)
    assert isinstance(resp, ReturnsResponse)
    ...


def test_inbound_booking_story(
        sample_client,
        return_request,
        sample_settings
):
    # book return shipment
    return_response = sample_client.create_return_shipment_order(return_request)
    dump_result_model(return_response)

    # convert addresses
    sender_address = return_request.shipment.return_address
    sender_address_verify = address_angonstic_to_verify_def(sender_address)

    # get DPS
    dps_request = AddressVerifyRequestDef(addresses=[sender_address_verify])
    dps_responses = sample_client.parcel_api.address_verify(dps_request)

    sender_address_verified = dps_responses[0]
    assert sender_address_verified.input.address_line1 == sender_address_verify.address_line1
    dps = sender_address_verified.dps
    postcode_and_dps = sender_address_verified.input.postcode.replace(' ', '') + dps

    # get collection slot
    item_count = 1
    slots_response = sample_client.parcel_api.slots_get_available(dps=postcode_and_dps, item_count=item_count)
    dump_result_model(slots_response)

    my_slot = match_date(slots_response, TEST_DATE)
    if my_slot is None:
        raise Exception('No slot found for date')
    token = slots_response.task_slots.slot_details.token_id
    ...
    # get services
    available_services_response = sample_client.check_return_services()
    serv = available_services_response.lookup_service_by_code(return_request.service.service_code)
    barcode_id = return_response.shipment.tracking_number

    dims = DimensionsPostDef(height=30, width=30, depth=30)
    item = ItemsPostDef(
        item_barcode_id=barcode_id,
        weight_in_grams=10000,
        item_service_name=serv.service_name,
        item_type=CollectionItemType.STANDARD,
        dimensions=dims,
    )

    # book collection
    dps_string = sender_address_verified.dps

    collection_address_mand = AddressMandatoryDef(**sender_address_verified.input.model_dump(), dps=dps_string)
    collection_address_non = AddressNonMandatoryDef(**sender_address_verified.input.model_dump(), dps=dps_string)
    sender_detials = SenderDetailsPostDef(sender_name='Test Sender', sender_email='TestSender@Email.com')
    account_details = AccountDetailsDef(retailer_account_number=sample_settings.account_number)
    collection_non_mand = Collection(
        timeslot_reservation_id=token,
        sender_details=sender_detials,
        account_details=account_details,
        address=collection_address_non,
        collection_date=TEST_DATE,
        items=[item],
    )

    collection_mand = CollectionMandatory(
        timeslot_reservation_id=token,
        sender_details=sender_detials,
        account_details=account_details,
        address=collection_address_mand,
        collection_date=TEST_DATE,
        items=[item],
    )

    dump_result_model(collection_mand)
    dump_result_model(collection_non_mand)
    order_resp = sample_client.parcel_api.collection_create_mandatory(collection=collection_mand)
    order_resp = sample_client.parcel_api.collection_create(collection=collection_non_mand)
    ...
    # order_resp = sample_client.parcel_api.collection_create_mandatory(collection=collection_mandatory)
    # dump_result_model(collection_payload)
    # order_resp = sample_client.parcel_api.collection_create(collection=collection_payload)
    ...

    # order_resp = sample_client.parcel_api.collection_create(collection=collection_payload)
