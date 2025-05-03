from fastapi import APIRouter, Depends, HTTPException, Query
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

@router.post("/", response_model=schemas.book.Book)
def create_book(book: schemas.book.BookCreate, db: Session = Depends(get_db)):
    return controllers.book.create_book(db, book)

@router.get("/", response_model=list[schemas.book.Book])
def list_books(search: str | None = Query(None), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return controllers.book.get_books(db, search, skip, limit)

@router.get("/{book_id}", response_model=schemas.book.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = controllers.book.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/{book_id}", response_model=schemas.book.Book)
def update_book(book_id: int, updates: schemas.book.BookUpdate, db: Session = Depends(get_db)):
    db_book = controllers.book.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return controllers.book.update_book(db, db_book, updates)

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = controllers.book.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    controllers.book.delete_book(db, db_book)