from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext

from src.config import settings
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encode_jwt(
        payload: dict,
        expire_minutes: int,
        private_key: str = settings.JWT_PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.JWT_ALGORITHM
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    token = jwt.encode(to_encode, private_key, algorithm)
    return token


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.JWT_PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.JWT_ALGORITHM
) -> dict:
    payload = jwt.decode(token, public_key, algorithms=[algorithm])
    return payload


def get_access_token(user: User) -> str:
    payload = {
        'sub': user.email,
        'email': user.email
    }
    access_token = encode_jwt(
        payload=payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return access_token


def get_refresh_token(user: User) -> str:
    payload = {
        'sub': user.email,
        'email': user.email
    }
    refresh_token = encode_jwt(
        payload=payload,
        expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    return refresh_token
