from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    available_copies: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True