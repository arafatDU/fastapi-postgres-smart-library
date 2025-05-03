# app/repositories/stats.py
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models import Book, Loan, User

class StatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_popular_books(self, limit: int = 10):
        stmt = (
            select(
                Book.id.label("book_id"),
                Book.title,
                Book.author,
                func.count(Loan.id).label("borrow_count")
            )
            .join(Loan, Book.id == Loan.book_id)
            .group_by(Book.id)
            .order_by(func.count(Loan.id).desc())
            .limit(limit)
        )
        return self.db.execute(stmt).all()

    def get_active_users(self, limit: int = 10):
        stmt = (
            select(
                User.id.label("user_id"),
                User.name,
                func.count(Loan.id).label("books_borrowed"),
                func.sum(func.coalesce(Loan.status == "ACTIVE", 0)).label("current_borrows")
            )
            .join(Loan, User.id == Loan.user_id)
            .group_by(User.id)
            .order_by(func.count(Loan.id).desc())
            .limit(limit)
        )
        return self.db.execute(stmt).all()

    def get_system_overview(self):
        total_books = self.db.query(func.count(Book.id)).scalar()
        total_users = self.db.query(func.count(User.id)).scalar()
        books_available = self.db.query(func.sum(Book.available_copies)).scalar()
        books_borrowed = self.db.query(func.count(Loan.id)).filter(Loan.status == "ACTIVE").scalar()
        overdue_loans = self.db.query(func.count(Loan.id)).filter(
            Loan.due_date < func.now(),
            Loan.status == "ACTIVE"
        ).scalar()
        
        today = func.date(func.now())
        loans_today = self.db.query(func.count(Loan.id)).filter(
            func.date(Loan.issue_date) == today
        ).scalar()
        
        returns_today = self.db.query(func.count(Loan.id)).filter(
            func.date(Loan.return_date) == today
        ).scalar()

        return {
            "total_books": total_books or 0,
            "total_users": total_users or 0,
            "books_available": books_available or 0,
            "books_borrowed": books_borrowed or 0,
            "overdue_loans": overdue_loans or 0,
            "loans_today": loans_today or 0,
            "returns_today": returns_today or 0
        }