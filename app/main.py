from fastapi import FastAPI
import os
from alembic import command
from alembic.config import Config
from app.models import init_db
from app.routers.user import user
from app.routers.auth import auth
from app.routers.article import article
from app.routers.label import label
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
def run_migrations():
    if os.environ.get('RUN_MIGRATIONS', 'true') == 'true':
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(user.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(article.router, prefix="/api/v1", tags=["articles"])
app.include_router(label.router, prefix="/api/v1", tags=["labels"])
