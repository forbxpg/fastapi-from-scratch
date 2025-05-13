import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


# CORS Middleware settings
ALLOW_CREDENTIALS = os.environ.get("ALLOW_CREDENTIALS").lower() == "true"
ALLOW_HEADERS = os.environ.get("ALLOW_HEADERS").split(",")
ALLOWED_METHODS = os.environ.get("ALLOW_METHODS").split(",")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS").split(",")


# Postgres
POSTGRES_URL = os.environ.get("POSTGRES_URL", "sqlite:///db.sqlite")


class SignUpSettings(BaseSettings):
    """Cognito signup secrets."""

    COGNITO_CLIENT_ID: str = ""
    COGNITO_CLIENT_SECRET: str = ""
    REGION_NAME: str = ""


# Constants
USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 150
