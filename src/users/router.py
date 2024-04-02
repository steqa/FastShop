import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from . import schemas, service, utils
from .dependencies import authenticate_user, get_current_auth_user
from .exceptions import (
    AuthError,
    MultiValidationError,
    NotAuthenticated,
    TokenInvalid,
    UserEmailExists,
    UserInactive,
    UserNotFound,
    UserPhoneNumberExists
)
from .models import User
from .pagination import Pagination

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)


@router.post(
    '/',
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example()
    ])
)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_auth_user)
):
    errors = []
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        errors.append(UserEmailExists)
    db_user = service.get_user_by_phone_number(
        db, phone_number=user.phone_number
    )
    if db_user:
        errors.append(UserPhoneNumberExists)
    if errors:
        raise MultiValidationError(
            errors, status_code=status.HTTP_409_CONFLICT
        )
    return service.create_user(db=db, user=user)


@router.get(
    '/',
    response_model=list[schemas.UserResponse],
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example()
    ])
)
def get_users(
        pagination: Pagination = Depends(),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_auth_user)
):
    users = service.get_users(db, pagination.skip, pagination.limit)
    return users


@router.post(
    '/login/',
    response_model=schemas.Token,
    responses=dict([
        AuthError.response_example(),
        UserInactive.response_example()
    ])
)
def login_user(user: User = Depends(authenticate_user)):
    access_token = utils.get_access_token(user)
    refresh_token = utils.get_refresh_token(user)
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='Bearer'
    )


@router.get(
    '/me/',
    response_model=schemas.UserResponse,
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example()
    ])
)
def get_current_user(current_user: User = Depends(get_current_auth_user)):
    return current_user


@router.get(
    '/{user_uuid}/',
    response_model=schemas.UserResponse,
    responses=dict([
        NotAuthenticated.response_example(),
        TokenInvalid.response_example(),
        UserNotFound.response_example()
    ])
)
def get_user(
        user_uuid: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_auth_user)
):
    user = service.get_user_by_uuid(db, user_uuid=user_uuid)
    if not user:
        raise UserNotFound
    return user
