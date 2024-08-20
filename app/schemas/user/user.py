from pydantic import BaseModel
from typing import List
from app.schemas.article.article import Article

class UserBase(BaseModel):
    name: str
    last_name:str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    articles: List[Article] = []

    class Config:
        orm_mode: True
