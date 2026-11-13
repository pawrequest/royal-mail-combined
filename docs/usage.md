# Usage guide

All examples assume:

```python
from royal_mail_combined import RoyalMailClient, all_models as m
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core.consts_types import (
    PackageFormat, RoyalMailServiceCodes, SendNotifcationsTo,
)

client = RoyalMailClient(RoyalMailSettingsGlobal.from_env())
```

`royal_mail_combined.all_models` re-exports every request/response model, so `m.CreateOrderRequest` and similar names work.

Every model inherits from `RMBaseModel`. You build it with snake_case field names, and it serialises to the camelCase
or PascalCase names the APIs expect (see [architecture.md](architecture.md#models)).

---

## 1. Outbound shipments (Click & Drop)

### Book

```python
from datetime import datetime

order = m.CreateOrderRequest(
    order_reference='INV-1234',
    order_date=datetime.now(),
    recipient=m.RecipientDetailsRequest(
        address=m.AddressRequest(
            full_name='Jane Doe', company_name='Acme Ltd',
            address_line1='1 High Street', city='London', postcode='NW1 1AA',
        ),
        phone_number='07000000000',
        email_address='jane@example.com',
    ),
    packages=[
        m.ShipmentPackageRequest(weight_in_grams=10_000, package_format_identifier=PackageFormat.PARCEL),
    ],
    postage_details=m.PostageDetailsRequest(
        service_code=RoyalMailServiceCodes.EXPRESS_24,
        send_notifications_to=SendNotifcationsTo.RECIPIENT,
        receive_email_notification=True,
        receive_sms_notification=True,
    ),
)
# order.add_label_request()  # ask Click & Drop to include the label in the create response

resp: m.CreateOrdersResponse = client.book_outbound(m.CreateOrdersRequest(items=[order]))
```

What `book_outbound` (`ClickAndDropClient.book_shipments`) does:

1. POSTs to `/orders` on Click & Drop.
2. Logs the response, leaving out the bulky `label` and `qr_code` fields.
3. **Raises `ApiException`** if any order is in `failed_orders`. Click & Drop answers a partial failure with HTTP 200,
   so without this check the failure would pass silently.

Useful response helpers: `resp.success_idents` (list of int ids), `resp.success_idents_str` (`'123;124'`, the format
the other order endpoints take), and `resp.error_messages`.

#### Automatic splitting for single-box services

Tracked 24 (`TPN24`), Tracked 24 Returns (`TSN`) and Special Delivery 1pm (`SD1`) accept **one package per order**.
When a `CreateOrdersRequest` holds an order on one of these services with more than one package, a model validator
replaces it with one order per package. Each new order's reference gets a suffix, for example `INV-1234 1/3 boxes`.
To check this yourself, use `core.helpers.should_split_rm_tracked_24(service_code, boxes)`.

> Only `PackageFormat.PARCEL` is known to work. See [known_rm_api_faults.md](../known_rm_api_faults.md).

### Fetch

```python
page = client.fetch_orders(page_size=50)                               # GetOrdersResponse (has continuation_token)
orders = client.fetch_specific_orders(order_identifiers='123;124')     # list[GetOrderInfoResource]
```

For the full detail variants, call the generated API directly:
`client.click_and_drop.orders_api.get_orders_with_details_async(...)` or `get_specific_orders_with_details_async(...)`.

**Order identifier strings:** integer ids are passed bare. String order references must be percent-encoded and wrapped
in double quotes. Separate several identifiers with `;`, up to 100 at a time.
`converters_no_import.order_identifiers_to_string([123, 'my ref'])` builds the string for you: `'123;"my%20ref"'`.

### Labels

```python
pdf: bytearray = client.get_label_data(
    order_identifiers=resp.success_idents_str,
    document_type='postageLabel',
    include_returns_label=False,
    include_cn=False,
)
Path('label.pdf').write_bytes(pdf)
```

The tests use the `pawdf` dependency (`pawdf.array_pdf.array_p.on_a4`) to tile labels onto A4 sheets.

### Cancel

```python
deleted = client.cancel_outbound_shipment(order_identifiers='123')
deleted.order_idents()       # ids/references that were actually deleted
```

> Labels on deleted orders become invalid. Royal Mail charges you, plus a handling fee, if a cancelled label is used.

### Manifests and version

These are only available through the generated API objects:

```python
client.click_and_drop.manifests_api.manifest_eligible_async(...)
client.click_and_drop.manifests_api.get_manifest_async(manifest_identifier=...)
client.click_and_drop.manifests_api.retry_manifest_async(manifest_identifier=...)
client.click_and_drop.version_api.get_version_async()
```

---

## 2. Inbound shipments (returns labels)

Return labels are booked through the Click & Drop `/returns` endpoint. The calls are written by hand in `RMHttpClient`,
because the endpoint is not in the Click & Drop swagger.

```python
sender = m.AddressReturns(        # where the parcel is collected from / the customer
    title='Mr', first_name='John', last_name='Smith',
    address_line1='Flat 43, Berberis House', address_line2='Highfield Road',
    city='Feltham', postcode='TW13 4GP', email='john@example.com',
)
recipient = m.AddressReturns(     # where the parcel goes back to (you)
    title='Mr', first_name='Returns', last_name='Dept', company_name='Acme Ltd',
    address_line1='70 Kingsgate Road', city='London', postcode='NW6 4TE', email='returns@example.com',
)

req = m.ReturnsRequest(
    service=m.Service(service_code=RoyalMailServiceCodes.TRACKED_24_RTN),
    shipment=m.ReturnShipment(recipient_address=recipient, sender_address=sender),
    # customer_reference defaults to sender company name, else sender full name
)

from royal_mail_combined.click_and_drop_api.models.return_models import ReturnRequestContainer
container = ReturnRequestContainer(return_requests=[req, req])   # one request per box

result = client.book_inbound_shipping(container)                 # ReturnResponseContainer
result.tracking_numbers, result.tracking_links, result.unique_ids
result.created_orders[0].label                                   # label data from the API
```

The returns endpoint books **one label per call**. `ReturnRequestContainer` lets you book several boxes at once. Its
validator requires every request in the container to have the **same service code, sender and recipient**, because it
represents one multi-box return.

Return service codes: `TRACKED_24_RTN` (`TSN`), `EXPRESS_24_RTN` (`RT0`), `EXPRESS_48_RTN` (`RTA`).

> There is **no cancel endpoint** for return labels. Contact your Royal Mail account manager to cancel one.

To list the return services enabled on the account:

```python
services = client.http_client.check_return_services()   # AvailableServicesResponse
services.lookup_service_by_code('TSN')
```

The `service_name` values this returns do **not** work with the Collection Order API. For collections, the library
uses the hard-coded `ReturnsServiceNames` enum instead (see `lookup_rtn_service_name`).

---

## 3. Returns with a doorstep collection

The combined workflow is `book_inbound_with_collection`:

```python
from datetime import date, timedelta

result = client.book_inbound_with_collection(
    container,
    collection_date=date.today() + timedelta(days=3),   # must be a date with an available slot
    box_dims=None,                                      # default DimensionsPostDef.large() = 32 x 24 x 63
    box_weight_kg=8,                                    # per box
)
result.tracking_numbers
result.collection_response.collection_order_id         # keep this to cancel later
result.collection_response.status                      # 'Order created successfully'
```

Steps it performs:

1. **Book return labels**, the same as `book_inbound_shipping`.
2. **Build collection items** with `ItemsPostDef.build_items_for_rtn_service`. It creates one item per tracking
   number, uses the return service code to pick the correct `ReturnsServiceNames` value, and sets the weight and
   dimensions.
3. **Verify the collection address** (the sender of the first return request) through Address `POST /address/dps`.
   This returns the address as Royal Mail holds it, plus the 2-character DPS.
4. **Reserve a slot.** It calls Collection Handler `GET /slots` with `dps = postcode-without-spaces + DPS` and the item
   count. It raises an error if `collection_date` is not among the returned `datewise_slots`. It then takes the
   response's `token_id`.
5. **Create the collection** through Collection Order `POST /collectionOrder/create` (`order_create_mandatory`), sending
   the slot token, sender details, your `ACCOUNT_NUMBER`, the verified address with its DPS, the date and the items.

If step 3, 4 or 5 fails, **the return labels from step 1 have already been created** and cannot be cancelled through
the API.

### Collection management

```python
client.cancel_collection('CC-W307-123456789')                                        # sets status to Cancelled
client.parcel_api.collection_orders_api.order_get('CC-W307-123456789')               # fetch
client.parcel_api.collection_orders_api.order_update(...)                            # update
client.parcel_api.collection_subscription_check(barcode, family_name, account_number) # product-family check
```

---

## 4. Addresses

```python
# Free-text search (minimum 12 characters)
found = client.address_search('70 Kingsgate Road NW6')          # AddressesDef -> .addresses: list[AddressSummaryDef]

# Retrieve full record by id from the search results
record = client.address_retrieve(address_id=found.addresses[0].address_id)

# Verify + get DPS for up to 100 addresses
verified = client.address_verify(m.AddressVerifiableList(addresses=[
    m.AddressVerifable(address_line1='70 Kingsgate Road', post_town='London', postcode='NW6 4TE'),
]))
verified[0].dps, verified[0].input
```

`client.parcel_api.verify_return_address(addr)` converts any address model that has `city` or `post_town` into an
`AddressVerifable`, then verifies it. It raises an error unless exactly one result comes back.

Some address records have a company name longer than 30 characters. `address_retrieve` therefore validates its result
into `AddressRecordDefPermissive`, a looser model than the spec's `AddressRecordDef`.

---

## 5. Tracking

```python
raw: dict = client.http_client.get_tracking(['BT112910032GB', 'BT112910033GB'])
```

This calls `GET https://api.royalmail.net/mailpieces/v2/summary?MailpieceId={...}`. There is no response model yet, so
the raw JSON is returned.

`core.endpoints.build_tracking_link(tracking_number)` builds the public royalmail.com tracking URL.

---

## 6. Errors

| Where                                     | Exception                                                     |
|-------------------------------------------|---------------------------------------------------------------|
| Generated API calls, non-2xx              | `core.exceptions.ApiException` subclasses (`BadRequestException`, `UnauthorizedException`, `NotFoundException`, `ServiceException`, …). The body is deserialised where possible |
| Hand-written `RMHttpClient` calls, non-2xx | `core.exceptions.RMStatusError2` (an `httpx.HTTPStatusError`) with `http_code`, `http_message`, `more_information` and `errors: list[RMError]` parsed from the Royal Mail error envelope. The failed request body is logged |
| Click & Drop create with failed orders    | `ApiException` that contains every failed order's error message |
| Invalid input                             | `pydantic.ValidationError`. Models and API methods validate input before any request is sent (`@validate_call`) |

---

## 7. Logging

The library logs with `loguru`. To use the bundled formatting:

```python
from royal_mail_combined.core.config_loguru import get_loguru
logger = get_loguru(level='DEBUG', profile='local')   # or profile='remote'
```

---

## 8. Scratch utilities

- `royal_mail_combined.one_shots`: small functions for manual operations such as `delete_order`, `cancel_collection`,
  `get_collection`, `check_available_rtn_srvcs` and `get_tracking_api`. Edit the `__main__` block and run the file.
  `delete_all_orders` is deliberately disabled.
- `royal_mail_combined.temp_client.temporary_client()`: a context manager that yields a client. On exit it deletes
  every Click & Drop order created inside the block. Use it for experiments against the live account.
