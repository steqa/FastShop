import uuid

from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate
from .utils import get_password_hash


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    del user.password_confirm
    del user.password
    user.email = user.email.lower()
    new_user = User(**user.model_dump(), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, skip: int, limit: int) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_uuid(db: Session, user_uuid: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_uuid).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def get_user_by_phone_number(db: Session, phone_number: str) -> User | None:
    return db.query(User).filter(User.phone_number == phone_number).first()
