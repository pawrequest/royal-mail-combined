import os
from datetime import date, timedelta

from royal_mail_combined.apis.parcels_apis.collection_handler.models import SlotDateDef
from royal_mail_combined.apis.returns.models import ReturnsResponse
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
    with open(r'dumped/ReturnsResponse.json', 'r') as f:
        data = f.read()
    rtn = ReturnsResponse.model_validate_json(data)
    labeldata = rtn.label
    label_bytes = decode_b64(labeldata)
    outp = r'dumped/return_label.pdf'
    with open(outp, 'wb') as f:
        f.write(label_bytes)
    os.startfile(outp)
    ...
