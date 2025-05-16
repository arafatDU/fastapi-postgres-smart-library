from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import services, schemas, database
from ..exceptions import ResourceNotFoundException, BadRequestException
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = services.user.get_user_by_email(db, user.email)
    if db_user:
        raise BadRequestException(detail="Email already registered")
    return services.user.create_user(db, user)

@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.user.get_user(db, user_id)
    if not db_user:
        raise ResourceNotFoundException(detail="User not found")
    return db_user

@router.get("/", response_model=list[schemas.user.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.user.get_users(db, skip, limit)

@router.put("/{user_id}", response_model=schemas.user.User)
def update_user(user_id: int, updates: schemas.user.UserUpdate, db: Session = Depends(get_db)):
    db_user = services.user.get_user(db, user_id)
    if not db_user:
        raise ResourceNotFoundException(detail="User not found")
    
    # If email is being updated, check for duplicates
    if updates.email and updates.email != db_user.email:
        existing_user = services.user.get_user_by_email(db, updates.email)
        if existing_user:
            raise BadRequestException(detail="Email already registered")
    
    return services.user.update_user(db, db_user, updates)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.user.get_user(db, user_id)
    if not db_user:
        raise ResourceNotFoundException(detail="User not found")
    services.user.delete_user(db, db_user)
    return {"message": "User deleted successfully"}