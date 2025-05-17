from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user, get_user, get_users, update_user, delete_user, get_user_by_email
from app.exceptions.http_exceptions import UserNotFoundException, EmailAlreadyExistsException
from app.database.init_db import get_db

router = APIRouter(tags=["users"])

@router.get("/", response_model=List[UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=UserRead)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise EmailAlreadyExistsException()
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise UserNotFoundException()
    return db_user

@router.put("/{user_id}", response_model=UserRead)
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated = update_user(db, user_id, user)
    if updated is None:
        raise UserNotFoundException()
    return updated

@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise UserNotFoundException()
    return {"ok": True}