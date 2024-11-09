from app.common.exceptions import NotFoundException, PasswordsDontMatchException
from app.common.utils import DeferredModel
from .repo import repo
from .dto import LoginDto
from .models import UserLoginInfo
from .auth import encode_user_login_info


def get_login_info(dto: DeferredModel[LoginDto]) -> tuple[UserLoginInfo, str]:
    valid_dto = dto.validate()

    user = repo.user_by_username(username=valid_dto.username)

    if not user:
        raise NotFoundException("User not found")

    if user["password"] != valid_dto.password:
        raise PasswordsDontMatchException()

    permissions_gen = repo.permissions_by_role(role_id=user["role_id"])
    permissions = list(map(lambda p: p["name"], permissions_gen))

    login_info = UserLoginInfo(username=user["username"], permissions=permissions)

    token = encode_user_login_info(login_info)

    return login_info, token
