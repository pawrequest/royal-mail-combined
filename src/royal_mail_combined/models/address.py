from typing import Annotated

from pydantic import Field, StringConstraints

from royal_mail_combined import RMBaseModel


class AddressFindRequestDef(RMBaseModel):
    """Address search string"""

    address_text: Annotated[
        str, StringConstraints(min_length=12, strict=True, max_length=200)
    ]