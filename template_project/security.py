from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from template_project.config import SecretTokenSettings, TokenSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_token_settings = SecretTokenSettings()  # type: ignore
token_settings = TokenSettings()  # type: ignore


def create_access_token(
    subject: str | Any,
    extra_options: dict = {},
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=token_settings.EXPIRATION_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    to_encode.update(extra_options)
    encoded_jwt = jwt.encode(
        to_encode,
        secret_token_settings.SECRET_KEY,
        algorithm=token_settings.ALGORITHM,
    )
    return encoded_jwt


def decode_jwt_token(token: str):
    return jwt.decode(
        token,
        key=secret_token_settings.SECRET_KEY,
        algorithms=[token_settings.ALGORITHM],
        options={"verify_exp": token_settings.VERIFY_EXPIRATION},
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
