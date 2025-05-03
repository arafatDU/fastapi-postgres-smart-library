from pydantic import BaseModel
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int
    available_copies: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    copies: int
    available_copies: int

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True