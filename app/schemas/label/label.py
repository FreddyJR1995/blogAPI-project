from pydantic import BaseModel

class LabelBase(BaseModel):
    text: str

class LabelCreate(LabelBase):
    pass

class Label(LabelBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
