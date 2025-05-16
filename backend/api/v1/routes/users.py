"""Module for user-related routes."""

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.users import UserRead, UserCreate
from api.v1.services import UserService
from database.db import get_session


user_router_v1 = APIRouter()


@user_router_v1.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    """Create a new user."""
    return await UserService(session).create_user(user, session)
