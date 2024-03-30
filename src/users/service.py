from sqlalchemy.orm import Session

from .auth import get_password_hash
from .models import User
from .schemas import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    user.password = get_password_hash(user.password)
    del user.password_confirm
    user.email = user.email.lower()
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, skip: int, limit: int) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> User | None:
    return db.query(User).filter(User.email == user_email.lower()).first()


def get_user_by_phone_number(db: Session, user_phone_number: str) -> User | None:
    return db.query(User).filter(User.phone_number == user_phone_number).first()