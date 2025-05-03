from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate):
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_book(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def update_book(self, book: Book):
        self.db.commit()
        self.db.refresh(book)
        return book

    def search_books(self, search_term: str):
        return self.db.query(Book).filter(
            (Book.title.ilike(f"%{search_term}%")) |
            (Book.author.ilike(f"%{search_term}%")) |
            (Book.isbn.ilike(f"%{search_term}%"))
        ).all()