from fastapi import FastAPI

from .db_tables import create_db_tables
from .users import router as users_router

app = FastAPI()

create_db_tables()

app.include_router(users_router.router)