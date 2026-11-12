# Reference: hand-written surface

This page covers the code written for this project. For the generated endpoint methods and models, the docstrings in
`click_and_drop_api/api/*.py` and `parcels_apis/*/api/*.py` (taken from the specs) are the reference, along with
`docs/swagger/`.

Every generated endpoint method `foo(...)` also has `foo_with_http_info(...)`, which returns an `ApiResponse` with
status, headers and raw bytes, and `foo_without_preload_content(...)`, which returns the raw urllib3 response. All of
them accept `_request_timeout`, `_request_auth`, `_content_type` and `_headers` overrides.

---

## `royal_mail_combined.RoyalMailClient`

`RoyalMailClient(settings: RoyalMailSettingsGlobal)`

| Attribute           | Type                  |
|---------------------|-----------------------|
| `settings`          | `RoyalMailSettingsGlobal` |
| `http_client`       | `RMHttpClient`        |
| `click_and_drop`    | `ClickAndDropClient`  |
| `parcel_api`        | `ParcelAPIClient`     |

### Bound shortcuts

| Shortcut                    | Target                                                    | Returns |
|-----------------------------|-----------------------------------------------------------|---------|
| `book_outbound(orders)`     | `click_and_drop.book_shipments`                           | `CreateOrdersResponse` (raises `ApiException` on any failed order) |
| `book_inbound_shipping(container)` | `http_client.book_inbound_shipment`                | `ReturnResponseContainer` |
| `fetch_orders(page_size=, start_date_time=, end_date_time=, continuation_token=)` | `orders_api.get_orders_async` | `GetOrdersResponse` |
| `fetch_specific_orders(order_identifiers)` | `orders_api.get_specific_orders_async`     | `list[GetOrderInfoResource]` |
| `get_label_data(order_identifiers, document_type='postageLabel', include_returns_label=False, include_cn=False)` | `labels_api.get_orders_label_async` | `bytearray` (PDF) |
| `cancel_outbound_shipment(order_identifiers)` | `orders_api.delete_orders_async`        | `DeleteOrdersResource` |
| `address_search(address_text)` | `parcel_api.address_search`                            | `AddressesDef` |
| `address_retrieve(address_id)` | `address_api.address_retrieve`                         | `AddressRecordDefPermissive` |
| `address_verify(addresses)` | `address_api.address_verify`                              | `list[AddressVerified]` |
| `cancel_collection(collection_id)` | `parcel_api.cancel_collection`                     | `CollectionOrderDeleteResponse` |

### `book_inbound_with_collection(return_request_container, collection_date, box_dims=None, box_weight_kg=8) -> ReturnResponseContainer`

Books the return labels, then a doorstep collection of those parcels from the sender address of the first request. The
result's `collection_response` holds the `CollectionOrderCreateResponse`. The steps are described in
[usage.md §3](usage.md#3-returns-with-a-doorstep-collection).

- `box_dims`: a `DimensionsPostDef`. The default is `DimensionsPostDef.large()` (32 × 24 × 63).
- `box_weight_kg`: the weight of each box, in whole kilograms.
- Raises `ValueError` if no slot token is returned, and `Exception('No slot found for date')` if `collection_date`
  is not available.

### `_book_collection_only(collection_address, collection_date, items) -> CollectionOrderCreateResponse`

Books only the collection, for parcels that already have labels. `items` is a `list[ItemsPostDef]`.

---

## `royal_mail_combined.royal_mail_client.RMHttpClient(BaseHttpClient)`

Endpoints written by hand with httpx. All of them use bearer auth.

| Method | HTTP | Returns |
|--------|------|---------|
| `book_inbound_shipment(container: ReturnRequestContainer)` | `POST {CAD_BASE}/returns`, once per request | `ReturnResponseContainer` |
| `check_return_services()` | `GET {CAD_BASE}/returns/services` | `AvailableServicesResponse`. The service names are **not** valid for collections |
| `get_tracking(tracking_numbers: str \| Collection[str])` | `GET mailpieces/v2/summary?MailpieceId={a,b}` | raw `dict` |

### `core.http_client.BaseHttpClient(settings)`

`do_get`, `do_post`, `do_put` and `do_delete` take keyword arguments only: `url`, plus `data` or `params`, plus
`headers`. A pydantic model passed as `data` or `params` is dumped with `mode='json', by_alias=True`. The default
headers are client-id/secret, the timeout is 30 s, and errors go through `raise_for_rm_status`.

---

## `click_and_drop_api.client.ClickAndDropClient(settings)`

| Member | |
|---|---|
| `orders_api: OrdersApi` | create, get, get full, get specific, delete, update status |
| `labels_api: LabelsApi` | `get_orders_label_async` |
| `manifests_api: ManifestsApi` | `manifest_eligible_async`, `get_manifest_async`, `retry_manifest_async` |
| `version_api: VersionApi` | `get_version_async` (no auth) |
| `book_shipment(order: CreateOrderRequest)` | wraps a single order in `CreateOrdersRequest`, then calls `book_shipments` |
| `book_shipments(orders: CreateOrdersRequest)` | creates the orders, logs the response without labels, raises `ApiException` if any order failed |

`failed_order_errors(response)` and `failed_order_errors2(response)` are module-level functions. Each raises
`ApiException` if the response has failed orders. `book_shipments` uses `failed_order_errors2`.

---

## `parcels_apis.client.ParcelAPIClient(settings)`

| Member | |
|---|---|
| `address_api: AddressApi` | `address_find`, `address_retrieve`, `address_verify` |
| `collection_orders_api: CollectionOrderApi` | `order_create`, `order_create_mandatory`, `order_get`, `order_update`, `order_delete` |
| `slots_api: GetAvailableSlotsApi` | `order_get_available_slots(dps, item_count)` |
| `subs_api: ProductFamilySubscriptionApi` | `order_validate_subscription(product_family)` |
| `address_search(address_text)` | text must be at least 12 characters, wrapped in `AddressFindRequest` |
| `verify_return_address(address)` | converts the address to `AddressVerifable`, calls `address_verify`, requires exactly one result. Returns `AddressVerified` |
| `get_token(collection_date, num_boxes, postcode_and_dps) -> str` | fetches slots, checks that `collection_date` is offered, returns `task_slots.slot_details.token_id` |
| `cancel_collection(collection_id)` | `order_delete` with status `CollectionStatus.CANCELLED` |
| `collection_subscription_check(barcode, family_name, account_number)` | product-family subscription validation |

`ReturnsCollectionApi.post_draft_collection_item` (`POST /collectionOrder/draftLabel`) exists in
`parcels_apis/collection_order/api`, but `ParcelAPIClient` does not create an instance of it.

---

## `config`

### `RoyalMailSettingsGlobal(BaseSettings)`

| Field | Env var | |
|---|---|---|
| `client_id: SecretStr` | `CLIENT_ID` | IBM gateway client id |
| `client_secret: SecretStr` | `CLIENT_SECRET` | IBM gateway client secret |
| `api_key: SecretStr` | `API_KEY` | Click & Drop bearer key |
| `account_number: str` | `ACCOUNT_NUMBER` | Royal Mail retailer account, used for collections |
| `data_dir: Path` | `DATA_DIR` | default `~/royal_mail_data` |

| Method | |
|---|---|
| `from_env(env_name='ROYAL_MAIL_ENV')` | loads the dotenv file whose path is in that env var. The result is cached (`lru_cache`) |
| `from_env_file(path)` | loads an explicit dotenv file |
| `authorised_headers_client()` | IBM id/secret headers plus base headers |
| `authorised_headers_bearer()` | bearer header plus base headers |
| `creds_dict()` | `{'Bearer', 'Client-Id', 'Client-Secret'}` for `Configuration.api_key` |
| `account_details` | `AccountDetailsDef(retailer_account_number=...)` |

Module functions: `get_env(env_name)` (checks that the var is set and the path exists), `base_headers()`,
`encode_b64_str(s)`.

---

## `core.consts_types` enums

| Enum | Values |
|---|---|
| `RoyalMailServiceCodes` | see [architecture.md](architecture.md#service-code-mapping) |
| `ReturnsServiceNames` | `TRACKED_24`, `EXPRESS_24_NEW`, `EXPRESS_48_NEW` |
| `PackageFormat` (Click & Drop) | `smallParcel`, `mediumParcel`, `parcel`, `letter`, `largeLetter`, `documents`, `undefined` |
| `LabelPackageFormat` | `Letter`, `LargeLetter`, `SmallParcel`, `MediumParcel` |
| `SendNotifcationsTo` | `sender`, `recipient`, `billing` |
| `CollectionStatus` | `Created`, `Pending`, `CollectionOrderPlaced`, `Collected`, `Cancelled`, `Processing`, `NotCollected`, `Attempted` |
| `ItemStatus` | `AwaitingCollection`, `Collected`, `NotCollected`, `Processing`, `Attempted` |
| `ResponseMessages` | `COLLECTION_CREATED = 'Order created successfully'`, `COLLECTION_CANCELLED = 'Order cancelled successfully'` |

Also defined there:

- `RMTracked24OneBoxOnly`: the list of single-box services.
- `lookup_rtn_service_name(code)`: maps a return service code to its `ReturnsServiceNames` value.

---

## Helpers

### `converters_no_import` (import-free; safe anywhere)

| Function | |
|---|---|
| `order_identifiers_to_string(ids)` | `[123, 'ref x']` → `'123;"ref%20x"'` |
| `order_identifier_to_string(id_or_ref)` | single-value version of the above |
| `order_idents_str(ids)` | plain `;` join, with no quoting |
| `created_orders_idents(resp)` / `created_orders_idents_str(resp)` | ids from a `CreateOrdersResponse` |
| `dps_postcode(verified)` | `postcode-without-spaces + DPS`, the format the slots endpoint expects |
| `match_collection_slot_date(slots, date)` | the `SlotDateDef` for that date, or `None` |

### `converters`

| Function | |
|---|---|
| `address_angonstic_to_verify_def(addr)` | any model with `address_line*` and `city`/`post_town`/`postcode` → `AddressVerifable` |
| `rtn_address_to_addr_verify(AddressReturns)` | → `AddressVerifable` |
| `addr_non_mandatory_from_addr(addr)` | → `AddressBasic` |
| `addr_mandatory_f_addr_and_dps(addr, dps)` | → `AddressDps` |
| `details_from_address(obj)` | any object with `full_name` and `email` → `SenderDetailsPostDef` |
| `convert_address(addr, typ)` | generic version. Only `AddressVerifable` is supported at present |

### `core.endpoints`

- `build_tracking_link(tracking_number)`: the public tracking page URL.
- `build_api_tracking_url(tracking_numbers)`: the URL for the tracking API summary.

### `core.helpers`

| Function | |
|---|---|
| `dump_result_model(model_or_list)` | prints the model, then writes JSON to `dumped-<YYYY-MM-DDTHH>/<Model>.json` |
| `print_object(obj)` | pretty-prints a model, list or dict |
| `get_dumped_dir_this_hour()` | the name of the current hour's dump directory |
| `should_split_rm_tracked_24(service_code, boxes)` | whether a booking must be split into one order per box |

### `core.exceptions`

| Name | |
|---|---|
| `ApiException` and its subclasses | raised by the generated API methods |
| `RMStatusError2` | raised by the hand-written httpx calls. Parses the Royal Mail error envelope into `http_code`, `http_message`, `more_information` and `errors: list[RMError(cause, code, description, resolution)]` |
| `raise_for_rm_status(response)` | raises `RMStatusError2` for a non-2xx response and logs the request body |
