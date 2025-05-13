"""User authentication module."""

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.db import get_db
from utils.auth_utils import generate_secret_hash
from schemas.users import SignUpRequest
from settings import SignUpSettings


router = APIRouter()


cognito = boto3.client(
    "cognito-idp",
    region_name=SignUpSettings.REGION_NAME,
)


@router.post("/signup")
def user_signup(
    request: SignUpRequest,
    db: Session = Depends(get_db()),
):
    """User signup endpoint."""
    try:
        response = cognito.sign_up(
            ClientId=SignUpSettings.COGNITO_CLIENT_ID,
            Username=request.email,
            Password=request.password,
            SecretHash=SignUpSettings.COGNITO_CLIENT_SECRET,
            ClientSecret=generate_secret_hash(
                request.email,
                SignUpSettings.COGNITO_CLIENT_ID,
                SignUpSettings.COGNITO_CLIENT_SECRET,
            ),
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": request.email,
                },
                {
                    "Name": "name",
                    "Value": request.name,
                },
            ],
        )
    except ClientError as e:
        error = e.response["Error"]["Code"]
        if error == "EntityAlreadyExists":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже существует.",
            )
        elif error == "InvalidPassword":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль не подходит под требования.",
            )
        else:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Регистрация провалена. {e}",
            )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка на стороне сервера.",
        )
    cognito_id = response.get("UserSub")
    if not cognito_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось вернуть валидный UserSub.",
        )
    new_user = User(
        name=request.name,
        email=request.email,
        cognito_id=cognito_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Вы успешно зарегистрировались в системе."}
