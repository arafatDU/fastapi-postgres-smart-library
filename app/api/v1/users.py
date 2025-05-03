# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    return UserService(db).create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_db)):
    user = UserService(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user