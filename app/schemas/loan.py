from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoanBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class LoanCreate(LoanBase):
    pass

class LoanReturn(BaseModel):
    loan_id: int

class LoanExtend(BaseModel):
    extension_days: int

class Loan(LoanBase):
    id: int
    issue_date: datetime
    return_date: Optional[datetime]
    status: str
    extensions_count: int

    class Config:
        from_attributes = True