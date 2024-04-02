from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.database import get_db
from . import schemas, service, utils
from .exceptions import AuthError, TokenInvalid, UserInactive
from .models import User

http_bearer = HTTPBearer()


def get_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    try:
        token = credentials.credentials
        payload = utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise TokenInvalid
    return payload


def get_current_auth_user(
        token_payload: dict = Depends(get_token_payload),
        db: Session = Depends(get_db)
) -> User:
    user_email = token_payload.get('email')
    user = service.get_user_by_email(db, email=user_email)
    if not user:
        raise TokenInvalid
    return user


def authenticate_user(
        user_data: schemas.UserLogin,
        db: Session = Depends(get_db)
) -> User:
    user = service.get_user_by_email(db, email=user_data.email)
    if not user:
        raise AuthError
    if not utils.validate_password(user_data.password, user.hashed_password):
        raise AuthError
    if not user.is_active:
        raise UserInactive
    return user
