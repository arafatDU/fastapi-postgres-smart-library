from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import controllers, schemas, database

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = controllers.user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return controllers.user.create_user(db, user)

@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controllers.user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[schemas.user.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return controllers.user.get_users(db, skip, limit)