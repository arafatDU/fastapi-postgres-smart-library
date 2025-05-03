# app/services/stats.py
from app.repositories.stats import StatsRepository
from app.schemas.stats import (
    PopularBooksResponse,
    ActiveUsersResponse,
    SystemOverviewResponse
)

class StatsService:
    def __init__(self, db):
        self.repo = StatsRepository(db)

    def get_popular_books(self, limit: int):
        results = self.repo.get_popular_books(limit)
        return [
            PopularBooksResponse(
                book_id=row.book_id,
                title=row.title,
                author=row.author,
                borrow_count=row.borrow_count
            ) for row in results
        ]

    def get_active_users(self, limit: int):
        results = self.repo.get_active_users(limit)
        return [
            ActiveUsersResponse(
                user_id=row.user_id,
                name=row.name,
                books_borrowed=row.books_borrowed,
                current_borrows=row.current_borrows
            ) for row in results
        ]

    def get_system_overview(self):
        data = self.repo.get_system_overview()
        return SystemOverviewResponse(**data)