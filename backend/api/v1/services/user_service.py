"""User services module."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.repositories.user_repository import UserRepository
from api.v1.schemas.users import UserCreate, UserRead


class UserService:
    """User service for managing users."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)

    async def check_user_exists(self, data: UserCreate) -> None:
        user = await self.user_repository.get_user_by_email(email=data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует!",
            )
        user = await self.user_repository.get_user_by_phone(phone=data.phone)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким номером телефона уже существует!",
            )

    async def create_user(self, data: UserCreate) -> UserRead:
        """Create a new user."""
        await self.check_user_exists(data)
        user = await self.user_repository.add_user(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=str(data.phone),
        )
        return UserRead(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=str(user.phone),
        )
