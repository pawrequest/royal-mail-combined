import json
from datetime import date, datetime, timedelta
from pathlib import Path
from pprint import pformat, pprint
from typing import Any, Generator

import pytest
from pydantic import BaseModel

from royal_mail_combined.added_models.services import RoyalMailServiceCodes
from royal_mail_combined.all_models import (
    AccountDetailsDef,
    AddressDef,
    AddressRequest,
    AddressReturns,
    AddressVerifyReqRespdef,
    AvailableServicesResponse,
    BillingDetailsRequest,
    CreateOrderRequest,
    CustomerReference,
    GetOrdersResponse,
    PostageDetailsRequest,
    RecipientDetailsRequest,
    ReturnsRequest,
    ReturnsResponse,
    SenderDetailsPostDef,
    Service,
    Shipment,
    ShipmentPackageRequest,
)
from royal_mail_combined.client_multi import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.consts_types import PackageFormat, SendNotifcationsTo
from royal_mail_combined.parcels_apis.address.models import AddressVerifyDef
from royal_mail_combined.parcels_apis.collection_handler.models import GetAvailableSlotsResponse

REFERENCE = 'TEST RETURN123456'
STORE_RESULTS = True

TEST_DATE = date.today() + timedelta(days=2)
if TEST_DATE.weekday() in (5, 6):
    TEST_DATE += timedelta(days=7 - TEST_DATE.weekday())


def get_dumped_dir_this_hour():
    return f"dumped-{datetime.now().strftime('%Y-%m-%dT%H')}"


def dump_result_model(result: BaseModel | list[BaseModel]):
    if isinstance(result, list):
        resmodel = result[0]
        result_d = [_.model_dump(mode='json', by_alias=True, exclude_none=True) for _ in result]
    elif isinstance(result, BaseModel):
        resmodel = result
        result_d = result.model_dump(mode='json', by_alias=True, exclude_none=True)
    else:
        raise ValueError('result must be BaseModel or list of BaseModel')

    dumped_dir = get_dumped_dir_this_hour()
    # dumped = f'dumped-{today().isoformat(sep='T')}'
    results_name = Path(f'{dumped_dir}/{resmodel.__class__.__name__}.json')
    results_name.parent.mkdir(parents=True, exist_ok=True)
    results_json = json.dumps(result_d)
    results_name.write_text(results_json)


@pytest.fixture(scope='session')
def sample_settings() -> RoyalMailSettingsGlobal:
    return RoyalMailSettingsGlobal.from_env()


def print_object(res: BaseModel):
    print(pformat(res.model_dump(mode='json'), indent=4, width=120))


@pytest.fixture(scope='session')
def sample_client(sample_settings) -> Generator[RoyalMailClient, Any, None]:
    """Test client - automatically removes orders created during testing on completion"""
    client = RoyalMailClient(sample_settings)
    orders_before: GetOrdersResponse = client.click_and_drop.fetch_orders()
    pprint(orders_before.model_dump())

    yield client

    orders_after: GetOrdersResponse = client.click_and_drop.fetch_orders()
    for o in orders_after.orders:
        if o not in orders_before.orders:
            print('Deleting Test Order')
            res = client.click_and_drop.delete_orders(order_identifiers=str(o.order_identifier))
            assert o.order_identifier in res.order_idents(), 'WARNING, FAILED TO DELETE TEST ORDERS!!'
            print('Deleted Test Orders')


@pytest.fixture(scope='session')
def cached_address() -> AddressDef:
    return AddressDef(
        addressLine1='Flat 43, Berberis House',
        addressLine2='Highfield Road',
        postTown='Feltham',
        County='Middlesex',  # mixed pascal and camel in rm api.
        postcode='TW13 4GP',
    )


@pytest.fixture(scope='session')
def cached_address_verify(cached_address) -> AddressVerifyDef:
    return AddressVerifyDef.model_validate(cached_address, from_attributes=True)


@pytest.fixture(scope='session')
def cached_return_address():
    return AddressDef(
        addressLine1='70 Kingsgate Road',
        postTown='Kilburn',
        County='London',
        postcode='NW64TE',
    )


@pytest.fixture(scope='session')
def cached_sender():
    return SenderDetailsPostDef(sender_name='Test Sender', sender_email='TestSender@Email.com')


@pytest.fixture(scope='session')
def cached_account_details(sample_settings):
    return AccountDetailsDef(retailer_account_number=sample_settings.account_number)


@pytest.fixture(scope='session')
def cached_slots_response():
    with open(r'data\collection_order_handler_get_slots.json') as f:
        res = f.read()
    return GetAvailableSlotsResponse.model_validate_json(res)


@pytest.fixture(scope='session')
def cached_address_id():
    return '068077252071149193225174041225027138078204116070010065014066078136091212102005045066044184012023'


@pytest.fixture(scope='session')
def cached_dps_results() -> AddressVerifyReqRespdef:
    with open(r'data\address_search_dps_results.json') as f:
        res = f.read()
        res = json.loads(res)
    return AddressVerifyReqRespdef.model_validate(res[0])


@pytest.fixture(scope='session')
def cached_return_request(cached_address, cached_sender, cached_return_address):
    sender_address = AddressReturns(
        title='Mr',
        first_name='ShipFirst',
        last_name='ShipLast',
        company_name='ShipCompany',
        address_line1=cached_address.address_line1,
        address_line2=cached_address.address_line2,
        address_line3=cached_address.address_line3,
        city=cached_address.post_town,
        county=cached_address.county,
        postcode=cached_address.postcode,
        country='United Kingdom',
        country_iso_code='GBR',
    )
    destination_address = AddressReturns(
        title='Mr',
        first_name='ReturnFirst',
        last_name='ReturnLast',
        company_name='ReturnCompany',
        address_line1=cached_return_address.address_line1,
        address_line2=cached_return_address.address_line2,
        address_line3=cached_return_address.address_line3,
        city=cached_return_address.post_town,
        county=cached_return_address.county,
        postcode=cached_return_address.postcode,
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
def address_request_recip_fxt():
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
def cached_address_req_sender():
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
def cached_recip_details(address_request_recip_fxt):
    return RecipientDetailsRequest(
        address=address_request_recip_fxt,
        phone_number='07666666666',
        email_address='recipient@sdgikhjbsdgijbsdigj.com',
    )


@pytest.fixture(scope='session')
def cached_billing(cached_address_req_sender):
    return BillingDetailsRequest(
        address=cached_address_req_sender,
        phone_number='07888888888',
        email_address='billme@sikdjfsdjbfgjksbdgf.com',
    )


@pytest.fixture(scope='session')
def cached_packages():
    return [
        ShipmentPackageRequest(
            weight_in_grams=10000,
            package_format_identifier=PackageFormat.PARCEL,
        )
        for _ in range(2)
    ]


@pytest.fixture(scope='session')
def cached_postage_details() -> PostageDetailsRequest:
    return PostageDetailsRequest(
        send_notifications_to=SendNotifcationsTo.RECIPIENT,
        service_code=RoyalMailServiceCodes.EXPRESS_24,
        receive_email_notification=True,
        receive_sms_notification=True,
        # is_local_collect=True,
    )


@pytest.fixture(scope='session')
def cached_order(cached_recip_details, cached_packages, cached_billing, cached_postage_details) -> CreateOrderRequest:
    return CreateOrderRequest(
        recipient=cached_recip_details.model_dump(),
        order_date=datetime.now(),
        subtotal=0,
        shipping_cost_charged=0,
        total=0,
        packages=cached_packages,
        billing=cached_billing,  # should be unnecessary with webportal settings
        postage_details=cached_postage_details,
        # planned_despatch_date=TEST_DATE,
    )
