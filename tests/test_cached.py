import os
from datetime import date, timedelta
from pathlib import Path

from conftest import get_dumped_dir
from royal_mail_combined.all_models import ReturnsResponse, SlotDateDef
from royal_mail_combined.converters import decode_b64, match_date


def test_my_slot(cached_slots_response):
    send_date = date.today() + timedelta(days=3)
    myslot = match_date(cached_slots_response, send_date)
    assert isinstance(myslot, SlotDateDef)


def test_loads_return_services(cached_return_services):
    assert cached_return_services.services
    for service in cached_return_services.services:
        assert service.carrier_guid


def test_label_from_return():
    dumped_dir = get_dumped_dir()
    with open(rf'{dumped_dir}/ReturnsResponse.json') as f:
        data = f.read()
    rtn = ReturnsResponse.model_validate_json(data)
    labeldata = rtn.label
    label_bytes = decode_b64(labeldata)
    outp = Path(rf'{dumped_dir}/return_label.pdf').absolute()
    with open(outp, 'wb') as f:
        f.write(label_bytes)
    os.startfile(outp)
    ...
