from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate, UserInDB


def create_user(db: Session, user: UserCreate) -> User:
    user_in_db = UserInDB(**user.model_dump(), hashed_password=user.password + '_fakehash')
    db_user = User(**user_in_db.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int, limit: int) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> User | None:
    return db.query(User).filter(User.email == user_email).first()


def get_user_by_phone_number(db: Session, user_phone_number: str) -> User | None:
    return db.query(User).filter(User.phone_number == user_phone_number).first()