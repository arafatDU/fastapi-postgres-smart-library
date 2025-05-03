from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import BaseModel

class Book(BaseModel):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    is_archived = Column(Boolean, default=False)