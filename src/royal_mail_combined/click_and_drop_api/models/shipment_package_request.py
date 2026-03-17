from __future__ import annotations

import re  # noqa: F401
from typing import Annotated

from pydantic import Field, StrictStr

from royal_mail_combined.core import RMBaseModel

from ..models.dimensions_request import DimensionsRequest
from ..models.product_item_request import ProductItemRequest


class ShipmentPackageRequest(RMBaseModel):
    weight_in_grams: Annotated[int, Field(le=30000, strict=True, ge=1)]
    package_format_identifier: StrictStr = Field(
        description="<b>If you have a ChannelShipper account, you can also pass the name of any of your custom package formats instead of the values below.</b><br> Enum: 'undefined', 'letter', 'largeLetter', 'smallParcel', 'mediumParcel', 'parcel', 'documents'",
        alias='packageFormatIdentifier',
    )
    custom_package_format_identifier: StrictStr | None = Field(
        default=None,
        description="This field will be deprecated in the future. Please use 'packageFormatIdentifier' for custom package formats from ChannelShipper.",
        alias='customPackageFormatIdentifier',
    )
    dimensions: DimensionsRequest | None = None
    contents: list[ProductItemRequest] | None = None
