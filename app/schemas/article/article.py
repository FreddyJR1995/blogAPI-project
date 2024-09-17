from pydantic import BaseModel
from typing import List, Optional, Type
from uuid import UUID
from app.schemas.label.label import Label, LabelCreate
from app.schemas.user.user_base import UserBase

class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: UUID

class ArticleCreate(BaseModel):
    title: str
    content: str
    labels: List[LabelCreate] = []

class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None

class Article(ArticleBase):
    id: UUID
    labels: List[Label] = []
    author: UserBase

    class Config:
        orm_mode = True
        from_attributes = True
