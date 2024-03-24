from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from . import schemas, service
from .pagination import Pagination

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)


@router.get('/', response_model=list[schemas.UserResponse])
def get_users(pagination: Pagination = Depends(), db: Session = Depends(get_db)):
    users = service.get_users(db, pagination.skip, pagination.limit)
    return users
