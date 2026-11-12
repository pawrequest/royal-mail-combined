# royal-mail-combined

A single Python client for several Royal Mail APIs that normally have to be used separately:

| Royal Mail API                    | Used for                                                        | Auth                 |
|-----------------------------------|-----------------------------------------------------------------|----------------------|
| **Click & Drop** (ChannelShipper) | Outbound orders, labels, manifests, returns labels              | Bearer API key       |
| **Address V1**                    | Address search, retrieve, DPS (Delivery Point Suffix) lookup    | IBM client id/secret |
| **Collection Order V1**           | Booking, fetching, updating and cancelling doorstep collections | IBM client id/secret |
| **Collection Order Handler V1**   | Available collection slots, product-family subscription checks  | IBM client id/secret |
| **Tracking V2** (minimal)         | Tracking summaries (raw JSON)                                   | Bearer               |

The main thing it adds on top of the raw APIs is **`RoyalMailClient.book_inbound_with_collection`**. In one call it
books return labels, checks the collection address, reserves a collection slot and books the doorstep collection.

## Requirements

- Python ≥ 3.13
- Royal Mail credentials:
    - a Click & Drop API key (bearer token)
    - an IBM API Gateway client id and secret (from the Royal Mail developer portal)
    - your Royal Mail account number (used for collections)

## Installation

The project builds with `uv`:

```bash
uv add git+<repo-url>         # as a dependency
# or, for development
uv sync
```

## Configuration

Settings are loaded by `RoyalMailSettingsGlobal` (`src/royal_mail_combined/config.py`), a `pydantic-settings` model.
Put the credentials in a dotenv file:

```dotenv
# royal_mail.env
CLIENT_ID=xxxxxxxx
CLIENT_SECRET=xxxxxxxx
API_KEY=xxxxxxxx           # Click & Drop bearer key
ACCOUNT_NUMBER=0123456789
# DATA_DIR=~/royal_mail_data   (optional)
```

Then point `ROYAL_MAIL_ENV` at that file:

```bash
export ROYAL_MAIL_ENV=/path/to/royal_mail.env
```

```python
from royal_mail_combined import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal

settings = RoyalMailSettingsGlobal.from_env()  # reads $ROYAL_MAIL_ENV (cached)
# settings = RoyalMailSettingsGlobal.from_env_file(Path('my.env'))  # or an explicit file
client = RoyalMailClient(settings)
```

Real environment variables with the same names also work, because this is standard `pydantic-settings` behaviour.

## Quick start

```python
from datetime import datetime
from royal_mail_combined.all_models import (
    AddressRequest, CreateOrderRequest, CreateOrdersRequest, PostageDetailsRequest,
    RecipientDetailsRequest, ShipmentPackageRequest,
)
from royal_mail_combined.core.consts_types import PackageFormat, RoyalMailServiceCodes
from royal_mail_combined import RoyalMailClient
from royal_mail_combined.config import RoyalMailSettingsGlobal

client = RoyalMailClient(RoyalMailSettingsGlobal.from_env())

order = CreateOrderRequest(
    order_reference='INV-1234',
    order_date=datetime.now(),
    recipient=RecipientDetailsRequest(
        address=AddressRequest(
            full_name='Jane Doe', address_line1='1 High Street', city='London',
            postcode='NW1 1AA', country_code='GB',
        ),
        email_address='jane@example.com',
    ),
    packages=[ShipmentPackageRequest(weight_in_grams=2000, package_format_identifier=PackageFormat.PARCEL)],
    postage_details=PostageDetailsRequest(service_code=RoyalMailServiceCodes.EXPRESS_24),
)

response = client.book_outbound(CreateOrdersRequest(items=[order]))
print(response.success_idents)  # Click & Drop order identifiers
label_pdf = client.get_label_data(order_identifiers=response.success_idents_str)
```

See **[docs/usage.md](docs/usage.md)** for every workflow: outbound, returns, collections, address lookup,
cancellation and tracking.

## Documentation

| Doc                                              | Contents                                                         |
|--------------------------------------------------|------------------------------------------------------------------|
| [docs/usage.md](docs/usage.md)                   | Task-oriented guide with examples                                |
| [docs/architecture.md](docs/architecture.md)     | Package layout, layers, auth, model conventions, errors, tests   |
| [docs/reference.md](docs/reference.md)           | Reference for the hand-written client surface, enums and helpers |
| [known_rm_api_faults.md](known_rm_api_faults.md) | Places where the real Royal Mail APIs differ from their docs     |
| `docs/swagger/`, `docs/*.pdf`                    | Upstream Royal Mail specs and technical guides (vendor material) |

## Development

```bash
uv sync
uv run pytest            # NOTE: the tests hit the live Royal Mail APIs, see docs/architecture.md#tests
```

Code style is `ruff` (line length 120, single quotes), run through `prek` (`prek.toml`).

## AI declaration:

APIs were generated by OpenAPIGenerator and modified by hand where necessary.
All other code was written by hand.
Docs (including this readme except this section) generated by Opus 5.5.