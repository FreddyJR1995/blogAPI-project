from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    last_name: str
    email: str 

    class Config:
        orm_mode = True
        from_attributes = True