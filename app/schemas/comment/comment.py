from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CommentBase(BaseModel):
    comment: str

class CommentCreate(CommentBase):
    article_id: UUID
    author_id: UUID

class CommentUpdate(CommentBase):
    comment: str

class Comment(CommentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    author_id: str
    article_id: str

    class Config:
        orm_mode = True
        from_attributes = True
