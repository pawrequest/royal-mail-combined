from __future__ import annotations

from datetime import date

from pydantic import Field, StrictFloat, StrictInt, StrictStr

from royal_mail_combined import RMBaseModel
from royal_mail_combined.models.consts_types import OptionalStrictNumber


class SlotDetailsDef(RMBaseModel):
    dps: str | None = None
    delivery_office_id: int | None = Field(
        default=None,
        description='Functional location id of Delivery office',
        alias='deliveryOfficeId',
    )
    item_count: StrictFloat | StrictInt | None = Field(default=None, description='count of Item.', alias='itemCount')
    token_id: StrictStr | None = Field(default=None, description='Token Id.', alias='tokenId')
    token_id_expiry_time: StrictStr | None = Field(
        default=None,
        description='Token id expiry time, within which it should be used to create task. This will be populated with the date time in ISO 8601 subset format.',
        alias='tokenIdExpiryTime',
    )


class EstimatedWindowDef(RMBaseModel):
    start_time: StrictStr | None = None
    end_time: StrictStr | None = None
    edw_visibility: OptionalStrictNumber = Field(default=None, description='EDW Visibility', alias='EDWVisibility')


class SlotDateDef(RMBaseModel):
    slot_date: date | None = None
    estimated_window: EstimatedWindowDef | None = None


class TaskSlotsDef(RMBaseModel):
    slot_details: SlotDetailsDef | None = None
    datewise_slots: list[SlotDateDef] = Field(default_factory=list)


class GetAvailableSlotsResponse(RMBaseModel):
    task_slots: TaskSlotsDef | None = Field(default=None, alias='taskSlots')

    def match_date(self, d: date) -> SlotDateDef | None:
        datewise = self.task_slots.datewise_slots or ()
        return next((_ for _ in datewise if _.slot_date == d), None)
