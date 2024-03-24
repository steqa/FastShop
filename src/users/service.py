from sqlalchemy.orm import Session

from .models import User


def get_users(db: Session, skip: int, limit: int) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()
