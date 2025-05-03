from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from app.models.base import BaseModel

class Loan(BaseModel):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)  # Add primary key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    status = Column(String(20), default="ACTIVE")
    extensions_count = Column(Integer, default=0)