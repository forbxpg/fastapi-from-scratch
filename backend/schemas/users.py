from pydantic import BaseModel


class SignUpRequest(BaseModel):
    """Model representing request data."""

    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    """Model representing request data."""

    email: str
    password: str
