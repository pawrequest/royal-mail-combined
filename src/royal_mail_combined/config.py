import base64
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Self

from loguru import logger
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from royal_mail_combined.parcels_apis.collection_order.models import AccountDetailsDef

RM_ENV_NAME = 'ROYAL_MAIL_ENV'


def encode_b64_str(s: str) -> str:
    return base64.b64encode(s.encode('utf8')).decode('utf8')


def get_env(env_name: str = RM_ENV_NAME) -> Path:
    env = os.getenv(env_name)
    if not env:
        raise ValueError(f'{env_name} not set')
    env_path = Path(env)
    if not env_path.exists():
        raise ValueError(f'{env_path} not a valid path')
    logger.debug(f'Loading environment from {env_path}')
    return env_path


def base_headers() -> dict:
    return {
        'X-RMG-Date-Time': datetime.now().isoformat(timespec='seconds'),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }


class RoyalMailSettingsGlobal(BaseSettings):
    client_id: SecretStr  # most RM APIs can use client-id/secret auth OR bearer
    client_secret: SecretStr
    api_key: SecretStr  # but 'click and drop' uses bearer only so need to support both
    account_number: str

    data_dir: Path = Path.home() / 'royal_mail_data'

    @classmethod
    @lru_cache
    def from_env(cls, env_name=RM_ENV_NAME) -> Self:
        return cls(_env_file=get_env(env_name))

    @classmethod
    def from_env_file(cls, env_file: Path) -> Self:
        return cls(_env_file=env_file)

    def authorised_headers_client(self) -> dict:
        heads = {
            'X-IBM-Client-Id': self.client_id.get_secret_value(),
            'X-IBM-Client-Secret': self.client_secret.get_secret_value(),
        }
        heads.update(base_headers())
        return heads

    def authorised_headers_bearer(self) -> dict:
        heads = {'Authorization': f'Bearer {self.api_key.get_secret_value()}'}
        heads.update(base_headers())
        return heads

    def creds_dict(self):
        return {
            'Bearer': self.api_key.get_secret_value(),
            'Client-Id': self.client_id.get_secret_value(),
            'Client-Secret': self.client_secret.get_secret_value(),
        }

    @property
    def account_details(self) -> AccountDetailsDef:
        return AccountDetailsDef(retailer_account_number=self.account_number)
