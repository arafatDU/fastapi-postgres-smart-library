from sqlalchemy.orm import Session
from ..models.book import Book
from ..schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, search: str | None = None, skip: int = 0, limit: int = 100):
    query = db.query(Book)
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, db_book: Book, updates: BookUpdate):
    for field, value in updates.model_dump().items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, db_book: Book):
    db.delete(db_book)
    db.commit()


def decrease_available_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book and book.available_copies > 0:
        book.available_copies -= 1
        db.commit()
        db.refresh(book)
        return book
    raise ValueError("Book is not available or does not exist")


def increase_available_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.available_copies += 1
        db.commit()
        db.refresh(book)
        return book
    raise ValueError("Book does not exist")