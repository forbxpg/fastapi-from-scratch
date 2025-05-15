"""User model for the database."""

import uuid

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

import settings


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String(settings.NAME_LENGTH), nullable=False)
    last_name = Column(String(settings.NAME_LENGTH), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    phone = Column(String(settings.PHONE_LENGTH), nullable=False, unique=True)
    email = Column(
        String(settings.EMAIL_LENGTH), nullable=False, unique=True, index=True
    )

    def __repr__(self):
        return f"Пользователь {self.first_name} {self.last_name}"
