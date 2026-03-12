import base64
import os
from datetime import date, timedelta
from pathlib import Path

from conftest import get_dumped_dir_this_hour, print_object
from royal_mail_combined.all_models import ReturnsResponse, SlotDateDef
from royal_mail_combined.converters import match_collection_slot_date


def test_my_slot(cached_slots_response):
    send_date = date.today() + timedelta(days=3)
    myslot = match_collection_slot_date(cached_slots_response, send_date)
    assert isinstance(myslot, SlotDateDef)


def test_loads_return_services(cached_return_services):
    assert cached_return_services.services
    for service in cached_return_services.services:
        assert service.carrier_guid
    print_object(cached_return_services)


def test_label_from_return():
    dumped_dir = get_dumped_dir_this_hour()
    dumped_dir = 'dumped-2026-03-06T21'
    with open(rf'{dumped_dir}/ReturnsResponse.json') as f:
        data = f.read()
    rtn = ReturnsResponse.model_validate_json(data)
    labeldata = rtn.label
    label_bytes = base64.b64decode(labeldata)
    outp = Path(rf'{dumped_dir}/return_label.pdf').absolute()
    with open(outp, 'wb') as f:
        f.write(label_bytes)
    os.startfile(outp)
    ...
