from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    role: str
    
    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    pass  

class UserRead(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True