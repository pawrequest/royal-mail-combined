import base64
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Self

from loguru import logger
from pydantic import SecretStr
from pydantic_settings import BaseSettings

RM_ENV_NAME = 'ROYAL_MAIL_COMBINED_ENV'


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


class RMSettings(BaseSettings):
    client_id: SecretStr
    client_secret: SecretStr
    api_key: SecretStr

    @classmethod
    @lru_cache
    def from_env(cls, env_name=RM_ENV_NAME) -> Self:
        return cls(_env_file=get_env(env_name))

    @classmethod
    def from_env_file(cls, env_file: Path) -> Self:
        return cls(_env_file=env_file)

    # @property
    def headers(self) -> dict:
        return {
            'X-IBM-Client-Id': self.client_id.get_secret_value(),
            'X-IBM-Client-Secret': self.client_secret.get_secret_value(),
            'X-RMG-Date-Time': datetime.now().isoformat(timespec='seconds'),
            'Content-Type': 'application/json',
        }