from sqlalchemy import Column, Integer, String, Enum
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum('student', 'faculty', name='user_roles'), nullable=False)