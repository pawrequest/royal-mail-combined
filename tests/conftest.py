import pytest

from royal_mail_combined.config import RMSettings


@pytest.fixture(scope="session")
def sample_settings() -> RMSettings:
    return RMSettings.from_env()