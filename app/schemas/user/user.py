from pydantic import BaseModel
from typing import List
from uuid import UUID
from app.schemas.article.article import Article
from app.schemas.user.user_base import UserBase

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    articles: List[Article] = []

    class Config:
        orm_mode = True
        from_attributes = True
