from royal_mail_combined.config_loguru import get_loguru
from royal_mail_combined.rm_basemodel import RMBaseModel
from royal_mail_combined.royal_mail_client import RoyalMailClient

# logger = get_loguru(level='DEBUG', profile='local')
__all__ = ['RMBaseModel', 'RoyalMailClient']
