from collections.abc import Generator
from datetime import date, datetime, timedelta
from pprint import pprint
from typing import Any

import pytest

from royal_mail_combined.all_models import (
    AccountDetailsDef,
    AddressRequest,
    AddressReturns,
    AddressVerifable,
    AvailableServicesResponse,
    BillingDetailsRequest,
    CreateOrderRequest,
    CustomerReference,
    GetAvailableSlotsResponse,
    GetOrdersResponse,
    PostageDetailsRequest,
    RecipientDetailsRequest,
    ReturnShipment,
    ReturnsRequest,
    ReturnsResponse,
    SenderDetailsPostDef,
    Service,
    ShipmentPackageRequest,
)
from royal_mail_combined.click_and_drop_api.models.return_models import ReturnRequestContainer
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.consts_types import PackageFormat, RoyalMailServiceCodes, SendNotifcationsTo
from royal_mail_combined.core.helpers import get_dumped_dir_this_hour
from royal_mail_combined.parcels_apis.address.models.address import AddressDefault
from royal_mail_combined.royal_mail_client import RoyalMailClient

REFERENCE = 'TEST RETURN123456'
STORE_RESULTS = True
TEST_SERVICES = [
    RoyalMailServiceCodes.TRACKED_24,
    RoyalMailServiceCodes.EXPRESS_24,
]

TEST_DATE = date.today() + timedelta(days=4)
if TEST_DATE.weekday() in (5, 6):
    TEST_DATE += timedelta(days=7 - TEST_DATE.weekday())


@pytest.fixture(scope='session')
def fxt_settings() -> RoyalMailSettingsGlobal:
    return RoyalMailSettingsGlobal.from_env()


@pytest.fixture(scope='session')
def fxt_client(fxt_settings) -> Generator[RoyalMailClient, Any]:
    """Test client - automatically removes orders created during testing on completion"""
    client = RoyalMailClient(fxt_settings)
    orders_before: GetOrdersResponse = client.fetch_orders()
    # pprint(orders_before.model_dump())

    yield client

    orders_after: GetOrdersResponse = client.fetch_orders()
    for o in orders_after.orders:
        if o not in orders_before.orders:
            print('Deleting Test Order')
            res = client.cancel_outbound_shipment(order_identifiers=str(o.order_identifier))
            assert o.order_identifier in res.order_idents(), 'WARNING, FAILED TO DELETE TEST ORDERS!!'
            print('Deleted Test Orders')


@pytest.fixture(scope='session')
def fxt_address() -> AddressDefault:
    return AddressDefault(
        address_line1='Flat 43, Berberis House',
        address_line2='Highfield Road',
        post_town='Feltham',
        County='Middlesex',  # mixed pascal and camel in rm api.
        postcode='TW13 4GP',
    )


@pytest.fixture(scope='session')
def fxt_address_verify(fxt_address) -> AddressVerifable:
    return AddressVerifable.model_validate(fxt_address, from_attributes=True)


@pytest.fixture(scope='session')
def cached_return_address():
    return AddressDefault(
        address_line1='70 Kingsgate Road',
        post_town='Kilburn',
        county='London',
        postcode='NW64TE',
    )


@pytest.fixture(scope='session')
def cached_sender():
    return SenderDetailsPostDef(sender_name='Test Sender', sender_email='TestSender@Email.com')


@pytest.fixture(scope='session')
def cached_account_details(fxt_settings):
    return AccountDetailsDef(retailer_account_number=fxt_settings.account_number)


@pytest.fixture(scope='session')
def cached_slots_response():
    dump_dir = get_dumped_dir_this_hour()
    with open(rf'{dump_dir}/GetAvailableSlotsResponse.json') as f:
        res = f.read()
    return GetAvailableSlotsResponse.model_validate_json(res)


@pytest.fixture(scope='session')
def cached_address_id():
    return '068077252071149193225174041225027138078204116070010065014066078136091212102005045066044184012023'


@pytest.fixture(scope='session')
def cached_return_response():
    with open(r'dumped/ReturnsResponse.json') as f:
        res = f.read()
    return ReturnsResponse.model_validate_json(res)


@pytest.fixture(scope='session')
def cached_return_services() -> AvailableServicesResponse:
    with open(r'dumped/AvailableServicesResponse.json') as f:
        # res_j = json.load(f)
        res = f.read()
    return AvailableServicesResponse.model_validate_json(res)


@pytest.fixture(scope='session')
def fxt_request_recip():
    return AddressRequest(
        full_name='Testy Testson Recipient',
        company_name='Recip Comp name',
        address_line1='addr line1',
        address_line2='',
        address_line3='',
        city='city',
        county='county',
        postcode='da163hu',
        country_code='GB',
    )


@pytest.fixture(scope='session')
def fxt_address_req_sender():
    return AddressRequest(
        full_name='MY SENDER NAME',
        company_name='MY COMPANY NAME',
        address_line1='MY FIRSTLINE',
        address_line2='',
        address_line3='',
        city='MY CITY',
        county='COUNTY',
        postcode='me88sp',
        country_code='GB',
    )


@pytest.fixture(scope='session')
def fxt_recip_details(fxt_request_recip):
    return RecipientDetailsRequest(
        address=fxt_request_recip,
        phone_number='07666666666',
        email_address='recipient@sdgikhjbsdgijbsdigj.com',
    )


@pytest.fixture(scope='session')
def fxt_billing(fxt_address_req_sender):
    return BillingDetailsRequest(
        address=fxt_address_req_sender,
        phone_number='07888888888',
        email_address='billme@sikdjfsdjbfgjksbdgf.com',
    )


@pytest.fixture(scope='session', params=[1, 2])
def fxt_packages(request):
    return [
        ShipmentPackageRequest(
            weight_in_grams=10000,
            package_format_identifier=PackageFormat.PARCEL,
        )
        for _ in range(request.param)
    ]


@pytest.fixture(scope='session', params=TEST_SERVICES)
def fxt_postage_details(request) -> PostageDetailsRequest:
    return PostageDetailsRequest(
        service_code=request.param,
        send_notifications_to=SendNotifcationsTo.RECIPIENT,
        receive_email_notification=True,
        receive_sms_notification=True,
    )


@pytest.fixture(scope='session')
def fxt_order(fxt_recip_details, fxt_packages, fxt_billing, fxt_postage_details) -> CreateOrderRequest:
    return CreateOrderRequest(
        order_reference=REFERENCE,
        recipient=fxt_recip_details,
        order_date=datetime.now(),
        packages=fxt_packages,
        # billing=fxt_billing,
        postage_details=fxt_postage_details,
    )


@pytest.fixture(scope='session')
def fxt_return_req():
    sender_address = AddressReturns(
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
        email='sender_emaiol@faaaaaaaaaaaaaaake.com',
    )
    recip_address = AddressReturns(
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
        email='recipient@faaaaaaake.com',
    )

    cust_ref = CustomerReference(reference=REFERENCE)
    service = Service(service_code=RoyalMailServiceCodes.TRACKED_24_RTN)
    return ReturnsRequest(
        service=service,
        shipment=ReturnShipment(
            recipient_address=recip_address,
            sender_address=sender_address,
            customer_reference=cust_ref,
        ),
    )


@pytest.fixture(scope='session', params=[1, 2])
def fxt_return_request_container(request, fxt_return_req) -> ReturnRequestContainer:
    return ReturnRequestContainer(return_requests=[fxt_return_req for _ in range(request.param)])
