from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

import settings


class PreBase:
    """Abstract base class for all database models."""

    @declared_attr
    def __tablename__(cls) -> str:
        return str(cls.__name__ + "s")

    id = Column(Integer, primary_key=True, index=True)


Base = declarative_base(cls=PreBase)


class User(Base):
    """User model in database."""

    cognito_id = Column(Text, unique=True, nullable=False, index=True)
    name = Column(String(settings.USERNAME_MAX_LENGTH), nullable=False)
    email = Column(
        String(settings.EMAIL_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"Пользователь {self.name}"
