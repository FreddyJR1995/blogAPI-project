from pydantic import BaseModel
from typing import List, Optional
from app.schemas.label.label import Label

class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: int

class ArticleCreate(ArticleBase):
    labels: List[Label] = []

class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None

class Article(ArticleBase):
    id: int
    labels: List[Label] = []

    class Config:
        orm_mode = True
