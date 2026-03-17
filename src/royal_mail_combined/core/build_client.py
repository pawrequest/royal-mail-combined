from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.core import ApiClient, Configuration


def build_client(settings: RoyalMailSettingsGlobal, host: str):
    config = Configuration()
    config.api_key = settings.creds_dict()
    config.host = host
    client = ApiClient(configuration=config)
    headers = {
        # 'X-RMG-Date-Time': datetime.now().isoformat(timespec='seconds'),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    client.default_headers.update(headers)
    return client
