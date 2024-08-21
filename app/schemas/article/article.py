from pydantic import BaseModel
from typing import List, Optional
from app.schemas.label.label import Label, LabelCreate

class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: int

class ArticleCreate(BaseModel):
    title: str
    content: str
    labels: List[LabelCreate] = []

class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None

class Article(ArticleBase):
    id: int
    labels: List[Label] = []

    class Config:
        orm_mode = True
