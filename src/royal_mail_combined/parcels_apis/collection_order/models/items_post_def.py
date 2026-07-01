from __future__ import annotations

from typing import Annotated, Self

from pydantic import Field, StrictFloat, StrictInt

from royal_mail_combined.core import RMBaseModel
from royal_mail_combined.core.consts_types import (
    ItemStatus,
    StrictStr5,
    StrictStr21,
    StrictStr40,
    StrictStr50,
    lookup_rtn_service_name,
)

from .collection_item_type import CollectionItemType
from .dimensions_post_def import DimensionsPostDef
from .label_info import LabelInfo


class ItemsPostDef(RMBaseModel):
    item_barcode_id: StrictStr21
    weight_in_grams: Annotated[int, Field(strict=True, ge=0)]
    item_service_name: StrictStr50
    dimensions: DimensionsPostDef
    item_reference: StrictStr40 | None = None
    item_status: ItemStatus | None = None
    item_price: StrictFloat | StrictInt | None = Field(
        default=None,
        description='Price paid for the doorstep collection for the item',
        alias='itemPrice',
    )
    item_type: CollectionItemType | None = None
    item_product_code: StrictStr5 | None = None
    label_info: LabelInfo | None = None

    @classmethod
    def build_items(
        cls,
        service_code: str,
        tracking_numbers: list[str],
        box_weight_kg: int = 8,
        box_dims: DimensionsPostDef | None = None,
        item_type: CollectionItemType = CollectionItemType.STANDARD,
    ) -> list[Self]:
        box_dims = box_dims or DimensionsPostDef.large()
        service_name = lookup_rtn_service_name(service_code)
        items = [
            cls(
                item_barcode_id=tracking_number,
                weight_in_grams=1000 * box_weight_kg,
                item_service_name=service_name,
                item_type=item_type,
                dimensions=box_dims,
            )
            for tracking_number in tracking_numbers
        ]
        return items
