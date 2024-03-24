from sqlalchemy.orm import Session

from .models import User


def get_users(db: Session) -> list[User]:
    return db.query(User).all()
