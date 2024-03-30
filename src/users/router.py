import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from . import schemas, service
from .exceptions import UserEmailExists, UserPhoneNumberExists
from .pagination import Pagination

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)


@router.post('/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise UserEmailExists
    db_user = service.get_user_by_phone_number(db, user_phone_number=user.phone_number)
    if db_user:
        raise UserPhoneNumberExists
    return service.create_user(db=db, user=user)


@router.get('/', response_model=list[schemas.UserResponse])
def get_users(pagination: Pagination = Depends(), db: Session = Depends(get_db)):
    users = service.get_users(db, pagination.skip, pagination.limit)
    return users


@router.get('/{user_id}', response_model=schemas.UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
