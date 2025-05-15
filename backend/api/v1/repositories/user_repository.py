"""User database interaction module."""

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


class UserRepository:
    """Repository for user data access."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_user_by_uuid(self, user_id: str) -> User: ...

    async def get_user_by_email(self, email: EmailStr) -> User: ...

    async def get_user_by_phone(self, phone: str) -> User: ...

    async def add_user(
        self, first_name: str, last_name: str, email: EmailStr, phone: str
    ) -> User:
        """Add a new user."""
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        self.db_session.add(user)
        await self.db_session.flush()
        return user
