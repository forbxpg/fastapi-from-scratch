"""API Utils."""

from typing import Union

from fastapi import HTTPException, status
from pydantic import GetJsonSchemaHandler, ValidationInfo
from phonenumbers import PhoneNumber as PhoneNumberTyping
from phonenumbers import (
    parse,
    NumberParseException,
    format_number,
    PhoneNumberFormat,
    is_valid_number,
)

import settings


class PhoneNumber(PhoneNumberTyping):
    """Phone number representation."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(
        cls,
        value: Union[str, PhoneNumberTyping],
        _validation_info: ValidationInfo,
    ) -> str:
        """Validate phone number."""
        if isinstance(value, PhoneNumberTyping):
            return str(value)
        try:
            parsed = parse(value, region=settings.PHONENUMBER_REGION)
            if not is_valid_number(parsed):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Некорректный номер телефона",
                )
        except NumberParseException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Некорректный номер телефона",
            )
        return format_number(parsed, PhoneNumberFormat.INTERNATIONAL)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema,
        handler=GetJsonSchemaHandler,
    ) -> dict:
        """Get JSON schema for phone number."""
        return {
            "type": "string",
            "format": "phone",
            "pattern": r"^\+?[1-9]\d{1,14}$",
            "examples": ["931234567", "934949191"],
            "description": "Phone number in international format.",
        }

    def json_encode(self) -> str:
        return format_number(self, PhoneNumberFormat.INTERNATIONAL)
