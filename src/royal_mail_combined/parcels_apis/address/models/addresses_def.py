from __future__ import annotations
import re  # noqa: F401

from .address_summary_def import AddressSummaryDef

from royal_mail_combined.core import RMBaseModel


class AddressesDef(RMBaseModel):
    """
    AddressesDef
    """

    addresses: list[AddressSummaryDef] | None = None
