import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from . import schemas, service, utils
from .dependencies import authenticate_user, get_current_auth_user
from .exceptions import (
    MultiValidationError,
    UserEmailExists,
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
)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
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
)
def get_users(
        pagination: Pagination = Depends(),
        db: Session = Depends(get_db),
):
    users = service.get_users(db, pagination.skip, pagination.limit)
    return users


@router.get(
    '/{user_uuid}/',
    response_model=schemas.UserResponse,
)
def get_user(
        user_uuid: uuid.UUID,
        db: Session = Depends(get_db),
):
    user = service.get_user_by_uuid(db, user_uuid=user_uuid)
    if not user:
        raise UserNotFound
    return user
