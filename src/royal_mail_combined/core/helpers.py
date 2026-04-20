import json
from datetime import datetime
from pathlib import Path
from pprint import pformat

from pydantic import BaseModel

from royal_mail_combined.core.consts_types import RMTracked24OneBoxOnly, RoyalMailServiceCodes


def get_dumped_dir_this_hour():
    return f'dumped-{datetime.now().strftime("%Y-%m-%dT%H")}'


def dump_result_model(result: BaseModel | list[BaseModel]):
    print_object(result)
    if result is None:
        print('No result to dump')
        return
    if isinstance(result, list):
        resmodel = result[0]
        result_d = [_.model_dump(mode='json', by_alias=True, exclude_none=True) for _ in result]
    elif isinstance(result, BaseModel):
        resmodel = result
        result_d = result.model_dump(mode='json', by_alias=True, exclude_none=True)
    else:
        raise ValueError('result must be BaseModel or list of BaseModel')
    dumped_dir = get_dumped_dir_this_hour()
    # dumped = f'dumped-{today().isoformat(sep='T')}'
    results_name = Path(f'{dumped_dir}/{resmodel.__class__.__name__}.json')
    results_name.parent.mkdir(parents=True, exist_ok=True)
    results_json = json.dumps(result_d)
    results_name.write_text(results_json)


def print_object(obj):
    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode='json', by_alias=True)
    if isinstance(obj, list):
        obj = [o.model_dump(mode='json', by_alias=True) if isinstance(o, BaseModel) else o for o in obj]
    print(pformat(obj, indent=4, width=120))


def should_split_rm_tracked_24(service_code: RoyalMailServiceCodes, boxes: int) -> bool:
    return boxes > 1 and service_code in RMTracked24OneBoxOnly
