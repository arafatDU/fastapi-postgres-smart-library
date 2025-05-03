from fastapi import HTTPException
from app.repositories.book import BookRepository
from app.schemas.book import BookCreate, BookResponse

class BookService:
    def __init__(self, db):
        self.repo = BookRepository(db)

    def create_book(self, book_data: BookCreate):
        return self.repo.create_book(book_data)

    def get_book(self, book_id: int):
        book = self.repo.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def update_book(self, book_id: int, update_data: dict):
        book = self.repo.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        for key, value in update_data.items():
            setattr(book, key, value)
        
        return self.repo.update_book(book)

    def search_books(self, search_term: str):
        return self.repo.search_books(search_term)