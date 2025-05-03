from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.book import BookResponse

class LoanBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class LoanCreate(LoanBase):
    pass

class LoanResponse(LoanBase):
    id: int
    issue_date: datetime
    return_date: datetime | None
    status: str
    book: BookResponse
    user: UserResponse

    class Config:
        from_attributes = True