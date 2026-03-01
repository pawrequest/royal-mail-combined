from royal_mail_combined.config_loguru import get_loguru
from royal_mail_combined.rm_base import RMBaseModel

logger = get_loguru(level='DEBUG', profile='local')
__all__ = ['RMBaseModel']