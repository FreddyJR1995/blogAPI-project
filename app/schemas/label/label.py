from pydantic import BaseModel
from uuid import UUID

class LabelBase(BaseModel):
    text: str

class LabelCreate(LabelBase):
    pass

class Label(LabelBase):
    id: UUID

    class Config:
        orm_mode = True
        from_attributes = True
