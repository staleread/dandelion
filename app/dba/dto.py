from typing import Annotated
from pydantic import StringConstraints

from app.common.utils import DeferrableModel


class LoginDto(DeferrableModel):
    username: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=3, max_length=30)
    ]
    password: Annotated[str, StringConstraints(pattern="^[A-Za-z\d]{3,}$")]
