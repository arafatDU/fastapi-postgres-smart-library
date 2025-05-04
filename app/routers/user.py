from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import services, schemas, database
from ..exceptions import ResourceNotFoundException, BadRequestException

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