from pydantic import field_validator, ValidationError

from app.common.utils.models import DeferrableModel


class LoginDto(DeferrableModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value) < 3:
            raise ValidationError("Ім'я користувача має містити щонайменше 3 символи")
        if len(value) > 30:
            raise ValidationError("Ім'я користувача має містити не більше 30 символів")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.isalnum():
            raise ValidationError("Пароль може містити лише літери та цифри")
        if len(value) < 3:
            raise ValidationError("Пароль має містити щонайменше 3 символи")
        return value


class CreateTableDto(DeferrableModel):
    title: str
    is_private: bool
    is_protected: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if len(value) < 3:
            raise ValidationError("Назва таблиці має містити щонайменше 3 символи")
        if len(value) > 30:
            raise ValidationError("Назва таблиці має містити не більше 30 символів")
        if not value.isascii():
            raise ValidationError("Назва таблиці може містити лише англійські літери")
        if not value.replace("_", "").islower():
            raise ValidationError("Назва таблиці не має містити великих літер")
        return value


class AttributeCreateDto(DeferrableModel):
    table_id: int
    name: str
    ukr_name: str
    data_type_id: int
    is_unique: bool = False
    is_nullable: bool = False

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValidationError("Назва атрибуту має містити щонайменше 2 символи")
        if len(value) > 30:
            raise ValidationError("Назва атрибуту має містити не більше 30 символів")
        if not value.isascii():
            raise ValidationError("Назва атрибуту може містити лише англійські літери")
        if not value.replace("_", "").islower():
            raise ValidationError("Назва атрибуту не має містити великих літер")
        return value

    @field_validator("ukr_name")
    @classmethod
    def validate_ukr_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValidationError("Українська назва має містити щонайменше 2 символи")
        if len(value) > 30:
            raise ValidationError("Українська назва має містити не більше 30 символів")
        return value

    @field_validator("data_type_id")
    @classmethod
    def validate_data_type_id(cls, value: int) -> int:
        if value < 1:
            raise ValidationError("Недопустимий тип даних")
        return value
