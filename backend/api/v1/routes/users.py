"""Module for user-related routes."""

from fastapi import APIRouter

from api.v1.schemas.users import UserRead, UserCreate
from api.v1.services import UserService
from database.db import async_session


user_router_v1 = APIRouter()


@user_router_v1.post("/", response_model=UserRead)
async def create_user(user: UserCreate) -> UserRead:
    """Create a new user."""
    async with async_session() as session:
        async with session.begin():
            user_service = UserService(session)
            return await user_service.create_user(user)
