from pydantic import BaseModel
from typing import List
from app.schemas.article.article import Article
from app.schemas.user.user_base import UserBase

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    articles: List[Article] = []

    class Config:
        orm_mode = True
