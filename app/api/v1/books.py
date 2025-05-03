# app/api/v1/books.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.book import BookService
from app.schemas.book import BookCreate, BookResponse
from app.core.database import get_db

router = APIRouter(prefix="/api/books", tags=["books"])

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db=Depends(get_db)):
    return BookService(db).create_book(book)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db=Depends(get_db)):
    return BookService(db).get_book(book_id)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, update_data: dict, db=Depends(get_db)):
    return BookService(db).update_book(book_id, update_data)

@router.get("/", response_model=list[BookResponse])
def search_books(search: str = "", db=Depends(get_db)):
    return BookService(db).search_books(search)