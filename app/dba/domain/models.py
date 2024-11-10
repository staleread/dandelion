from pydantic import BaseModel, ConfigDict


class UserLoginInfo(BaseModel):
    # ignore JWT claims
    model_config = ConfigDict(extra="ignore")

    username: str
    permissions: list[str]
