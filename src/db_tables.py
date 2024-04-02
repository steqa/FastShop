from .database import engine
from .users import models as users_models


def create_db_tables():
    users_models.Base.metadata.create_all(bind=engine)
