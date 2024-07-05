from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    last_name:str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode: True
