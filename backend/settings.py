"""Settings for the backend application."""

import os
import re

from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)
DATABASE_ECHO = (
    os.environ.get("DATABASE_ECHO", default="false").lower() == "true"
)

# Constants
NAME_LENGTH = 150
EMAIL_LENGTH = 254
PHONE_LENGTH = 20
PHONENUMBER_REGION = "UZ"


# Validation
LETTER_PATTERN = re.compile(r"^[a-zA-Zа-яА-ЯёЁ]+$")

# CORS Middleware settings
ALLOW_CREDENTIALS = os.environ.get("ALLOW_CREDENTIALS").lower() == "true"
ALLOW_HEADERS = os.environ.get("ALLOW_HEADERS").split(",")
ALLOWED_METHODS = os.environ.get("ALLOW_METHODS").split(",")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS").split(",")


# Postgres
POSTGRES_URL = os.environ.get("POSTGRES_URL", "sqlite:///db.sqlite")
