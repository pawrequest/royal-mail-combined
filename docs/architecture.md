# Architecture

## Package layout

```
src/royal_mail_combined/
├── __init__.py               exports RoyalMailClient, all_models
├── royal_mail_client.py      ★ RoyalMailClient (facade) + RMHttpClient (hand-written endpoints)
├── config.py                 ★ RoyalMailSettingsGlobal, auth header builders
├── all_models.py             re-export of every model from every sub-API
├── converters.py             address model conversions (import-time dependencies)
├── converters_no_import.py   pure helpers (order-identifier encoding, slot matching, DPS string)
├── one_shots.py              manual scratch operations
├── temp_client.py            context manager that cleans up test orders
│
├── core/                     shared transport + base types
│   ├── rm_basemodel.py       ★ RMBaseModel (alias conventions)
│   ├── consts_types.py       ★ enums (service codes, package formats, statuses), constrained str types
│   ├── endpoints.py          ★ base URLs, tracking URL builders
│   ├── build_client.py       ★ build_client(settings, host) -> configured ApiClient
│   ├── http_client.py        ★ BaseHttpClient: thin httpx wrapper used by RMHttpClient
│   ├── exceptions.py         generated ApiException hierarchy + ★ RMStatusError2 / raise_for_rm_status
│   ├── helpers.py            dump/print helpers, should_split_rm_tracked_24
│   ├── config_loguru.py      loguru setup
│   ├── core_api_client.py    ApiClient (OpenAPI-generator, adapted)
│   ├── configuration.py      Configuration incl. auth_settings (adapted)
│   ├── rest.py, api_response.py   urllib3 transport + ApiResponse (generated)
│
├── click_and_drop_api/
│   ├── client.py             ★ ClickAndDropClient (book_shipment(s), failed-order checking)
│   ├── api/                  OrdersApi, LabelsApi, ManifestsApi, VersionApi (generated, lightly edited)
│   └── models/               generated models + ★ return_models.py (hand-written returns models)
│
└── parcels_apis/
    ├── client.py             ★ ParcelAPIClient (address verify, slots/token, cancel collection)
    ├── address/              AddressApi + models (address.py is ★ hand-written)
    ├── collection_handler/   GetAvailableSlotsApi, ProductFamilySubscriptionApi + models
    ├── collection_order/     CollectionOrderApi, ReturnsCollectionApi + models
    └── common_models/        shared error envelopes (Model400 … Model503, ErrorsDef)
```

★ marks code that is hand-written or substantially hand-edited. Everything else came from OpenAPI Generator, run on the
specs in `docs/swagger/`. It has since been adapted: pydantic v2, `RMBaseModel`, Python 3.13 syntax, and response maps
fixed where the specs are wrong.

## Layers

```
RoyalMailClient                      ← facade; aliases + multi-API workflows
├── RMHttpClient (BaseHttpClient)    ← httpx; endpoints missing from the specs (returns, tracking)
├── ClickAndDropClient               ← host CAD_BASE
│   └── OrdersApi / LabelsApi / ManifestsApi / VersionApi
└── ParcelAPIClient
    ├── AddressApi                   ← host ADDRESS_BASE
    ├── CollectionOrderApi           ← host ORDERS_NET
    └── GetAvailableSlotsApi / ProductFamilySubscriptionApi  ← host COLLECTION_HANDLER_NET
        (all generated APIs share: ApiClient → RESTClientObject → urllib3)
```

**`RoyalMailClient`** has no logic for single API calls. It binds the most-used methods of the sub-clients as
attributes (`book_outbound`, `fetch_orders`, `address_search`, `cancel_collection`, …) so callers have one flat surface.
The only real logic it holds is the multi-API workflow `book_inbound_with_collection` / `_book_collection_only`, which
chains Click & Drop returns → Address DPS → Collection Handler slots → Collection Order create.

The sub-clients stay public (`client.click_and_drop`, `client.parcel_api`, `client.http_client`), so you can reach
every generated endpoint.

## Hosts

Defined in `core/endpoints.py`:

| Constant                 | URL                                             |
|--------------------------|-------------------------------------------------|
| `CAD_BASE`               | `https://api.parcel.royalmail.com/api/v1`       |
| `RETURNS_ENDPOINT`       | `CAD_BASE + /returns`                           |
| `RETURNS_SERVICES_ENDPOINT` | `CAD_BASE + /returns/services`               |
| `ADDRESS_BASE`           | `https://api.royalmail.net/addressfind/v1`      |
| `ORDERS_NET`             | `https://api.royalmail.net/orders/v1` (Collection Order) |
| `COLLECTION_HANDLER_NET` | `https://api.royalmail.net/collectionorders/v1` |
| `API_TRACKING_URL`       | `https://api.royalmail.net/mailpieces/v2`       |

## Authentication

There are two schemes, and `RoyalMailSettingsGlobal` holds the credentials for both:

| Scheme                       | Headers                                         | Used by |
|------------------------------|-------------------------------------------------|---------|
| Bearer (`API_KEY`)           | `Authorization: Bearer …`                       | Click & Drop (orders, labels, manifests, returns), tracking |
| IBM client credentials       | `X-IBM-Client-Id`, `X-IBM-Client-Secret`        | Address, Collection Order, Collection Handler |

How they are applied:

- **Generated APIs.** `build_client()` puts `settings.creds_dict()` (`Bearer`, `Client-Id` and `Client-Secret` keys)
  into `Configuration.api_key`. Each generated method declares `_auth_settings` (for example `['Bearer']` or
  `['Client-Id', 'Client-Secret']`). `Configuration.auth_settings()` maps those names to headers, and
  `ApiClient.update_params_for_auth` applies them.
- **Hand-written calls.** `BaseHttpClient.do_*` use `settings.authorised_headers_client()` by default.
  `RMHttpClient` passes `authorised_headers_bearer()` explicitly for returns and tracking. Both header builders also add
  `X-RMG-Date-Time` (now, ISO seconds), `Content-Type` and `Accept`.
- Generated Parcel API methods need an `x_rmg_date_time` header parameter. Its type is `DatetimeNowIsoSeconds`, which
  defaults to the current time, so callers never pass it.

## Models

All models inherit from `core.rm_basemodel.RMBaseModel`:

```python
ConfigDict(
    alias_generator=AliasGenerator(alias=to_camel),
    validate_by_alias=True, validate_by_name=True, populate_by_name=True,
    use_enum_values=True,
)
```

- Write snake_case in Python. The model emits camelCase.
- Royal Mail is inconsistent: some fields are PascalCase (`DPS`, `County`, `Addresses`, `Input`, `ServiceRegisterCode`,
  `IOSSNumber`). Those fields set an explicit `alias=`. Keep these when you regenerate or edit models.
- Serialise with `model_dump(mode='json', by_alias=True)`. `BaseHttpClient` and `ApiClient.sanitize_for_serialization`
  already do this. The generated path also passes `exclude_none=True`, so unset optional fields are left out of the
  request.
- Enums are stored as their values (`use_enum_values`), so `StrEnum` members can go into `StrictStr` fields.
- `core.consts_types` holds length-limited strict string aliases (`StrictStr10`, `StrictStr64`, …) that mirror the spec
  limits, so overlong values fail before the request is sent.

### Hand-written model families

- **Address hierarchy** (`parcels_apis/address/models/address.py`). Each step makes more fields required:
  `AddressDefault` (all optional) → `AddressBasic` (line1, postcode) → `AddressVerifable` (+ post_town) →
  `AddressDps` (+ DPS). `LabelAddress` is a variant with a camelCase `county` and a default DPS of `9Z`.
  `CollectionMandatory.address` must be an `AddressDps`.
- **Returns models** (`click_and_drop_api/models/return_models.py`). These cover the `/returns` endpoint, which is
  missing from the Click & Drop swagger: `ReturnsRequest`, `ReturnShipment`, `AddressReturns`, `Service`,
  `ReturnsResponse`, `AvailableServicesResponse`. There are also two containers: `ReturnRequestContainer` (multi-box,
  same service, sender and recipient) and `ReturnResponseContainer` (labels plus an optional collection response).
- **Model helpers.** These are added to generated models:
  - `CreateOrdersRequest.tracked24_one_package_per_order` splits multi-box orders on single-box services.
  - `CreateOrdersResponse.success_idents` / `error_messages`.
  - `CreateOrderRequest.add_label_request`.
  - `DeleteOrdersResource.order_idents`.
  - `ItemsPostDef.build_items_for_rtn_service`.
  - `DimensionsPostDef.small()` / `large()`.

## Service-code mapping

`RoyalMailServiceCodes` (`core/consts_types.py`) is the one place the library defines service codes:

| Member            | Code    | Notes                                      |
|-------------------|---------|--------------------------------------------|
| `TRACKED_24`      | `TPN24` | one box per order                          |
| `SPECIAL_1PM`     | `SD1`   | one box per order                          |
| `EXPRESS_24`      | `NDA`   | Parcelforce express24                      |
| `EXPRESS_48`      | `FEO`   | Parcelforce express48                      |
| `EXPRESS_AM`      | `FEE`   | unverified                                 |
| `EXPRESS_10`      | `TE1`   | unverified                                 |
| `TRACKED_24_RTN`  | `TSN`   | return; one box per order                  |
| `EXPRESS_24_RTN`  | `RT0`   | return                                     |
| `EXPRESS_48_RTN`  | `RTA`   | return                                     |

The Collection Order API needs an `itemServiceName`. The value `/returns/services` reports is wrong for this, so
`lookup_rtn_service_name()` maps return codes to the hard-coded values that Royal Mail support supplied
(`ReturnsServiceNames`):

| Return code | `item_service_name`                    |
|-------------|----------------------------------------|
| `TSN`       | `Tracked Returns 24 (T24) Enhanced`    |
| `RT0`       | `express24`                            |
| `RTA`       | `express48`                            |

## Error handling

- **Generated path.** `ApiClient.response_deserialize` uses each method's `_response_types_map` to pick a model by
  status code. Non-2xx responses go through `ApiException.from_response`, which raises the matching subclass
  (`BadRequestException` 400, `UnauthorizedException` 401, `ForbiddenException` 403, `NotFoundException` 404,
  `ConflictException` 409, `UnprocessableEntityException` 422, `ServiceException` 5xx).
- **Hand-written path.** `raise_for_rm_status()` wraps `httpx.HTTPStatusError` in `RMStatusError2`, parses the Royal
  Mail error envelope (`httpCode`, `httpMessage`, `moreInformation`, `message`, `errors[]`) and logs the failed request
  body.
- **Response maps that differ from the specs.** These have been edited by hand to match what the API actually returns,
  for example `order_create_mandatory` also accepts `200` (the spec says `201`). They are marked with a comment. If you
  regenerate, re-apply them, and add new ones to [known_rm_api_faults.md](../known_rm_api_faults.md).

## Regenerating from specs

The generated code has been edited a lot (model base class, aliases, helper methods, response maps). If you regenerate,
diff the output against the current code instead of overwriting it. The specs are:

| Spec in `docs/swagger/`                                   | Package                           |
|-----------------------------------------------------------|-----------------------------------|
| `click-and-drop-api-v1.yaml`                              | `click_and_drop_api`              |
| `Royal_Mail_Address_V1_(REST)-1.0.9.json`                 | `parcels_apis/address`            |
| `Royal_Mail_Order_V1_(REST)-1.0.44.json`                  | `parcels_apis/collection_order`   |
| `Royal_Mail_Collection_Order_Handler_V1_(REST)-1.0.20.json` | `parcels_apis/collection_handler` |
| Tracking / Delivery Office Finder / Local Collect         | not implemented                   |

## Tests

`tests/` are **live integration tests**. They need a valid `ROYAL_MAIL_ENV` and they create real orders, return labels
and collections on the account.

- The `fxt_client` fixture (session-scoped) records the existing Click & Drop orders when the session starts. At
  teardown it **deletes any order created during the session**.
- **Return labels cannot be cancelled.** `test_book_inbound*` therefore creates real returns that stay on the account.
  `test_book_inbound_with_collection_cancel_collection` cancels the collection it books, but not the labels.
- Fixtures are parametrised over services (`TEST_SERVICES`, `TEST_RETURN_SERVICES`) and box counts (1, 2), so a full
  run makes many bookings.
- `TEST_DATE` is today + 4 days, moved forward past weekends.
- `dump_result_model` writes responses to `dumped-YYYY-MM-DDTHH/<Model>.json` (gitignored). Some `cached_*` fixtures
  read them back.
- `test_x_fails.py` is a stub for failure cases. It currently asserts nothing.

Run a subset, for example `uv run pytest tests/test_live.py -k address`.
