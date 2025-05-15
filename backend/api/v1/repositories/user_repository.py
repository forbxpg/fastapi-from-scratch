"""Модуль для интерфейса пользователей с БД."""

import uuid

from phonenumbers import (
    NumberParseException,
    format_number,
    PhoneNumberFormat,
    parse,
)
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from settings import PHONENUMBER_REGION


class UserRepository:
    """Класс для работы с пользователями в БД."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_user_by_uuid(self, user_id: uuid.UUID) -> User | None:
        """Метод для получения пользователя по uuid."""
        result = await self.db_session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        """Метод для получения пользователя по email."""
        result = await self.db_session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str) -> User:
        """Метод для получения пользователя по номеру телефона."""
        try:
            phone = parse(phone, PHONENUMBER_REGION)
            phone = format_number(phone, PhoneNumberFormat.INTERNATIONAL)
        except NumberParseException:
            raise ValueError("Формат номера неверный.")
        result = await self.db_session.execute(
            select(User).where(User.phone == phone)
        )
        return result.scalar_one_or_none()

    async def add_user(
        self, first_name: str, last_name: str, email: EmailStr, phone: str
    ) -> User:
        """Метод для создания пользователя в БД."""
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        self.db_session.add(user)
        await self.db_session.flush()
        return user
