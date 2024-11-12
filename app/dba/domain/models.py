from pydantic import BaseModel, ConfigDict

from app.dba.data.models import Permission


class UserLoginInfo(BaseModel):
    # ignore JWT claims
    model_config = ConfigDict(extra="ignore")

    username: str
    permissions: list[Permission]
