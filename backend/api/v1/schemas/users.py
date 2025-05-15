"""Pydantic-модели для пользователей."""

from fastapi import HTTPException, status
from pydantic import field_validator, EmailStr, UUID4
from pydantic import BaseModel as PydanticBaseModel

from .utils import PhoneNumber
from settings import LETTER_PATTERN


class BaseModel(PydanticBaseModel):
    """Базовая модель для юзеров.."""

    class Config:
        """Конфиг pydantic для взаимодействия с не-json объектами."""

        orm_mode = True
        arbitrary_types_allowed = True


class UserRead(BaseModel):
    """Модель для репрезентации пользователя."""

    user_id: UUID4
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    class Config(BaseModel.Config):
        """Pydantic configuration."""

        json_encoders = {
            PhoneNumber: PhoneNumber.json_encode,
        }


class UserCreate(BaseModel):
    """Модель для создания пользователя."""

    first_name: str
    last_name: str
    email: EmailStr
    phone: PhoneNumber

    class Config(BaseModel.Config):
        """Pydantic configuration."""

        json_encoders = {
            PhoneNumber: PhoneNumber.json_encode,
        }

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value: str) -> str:
        if not LETTER_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя может содержать только буквы",
            )
        return value

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: str) -> str:
        if not LETTER_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Фамилия может содержать только буквы",
            )
        return value
