# app/api/v1/stats.py
from fastapi import APIRouter, Depends
from app.services.stats import StatsService
from app.schemas.stats import (
    PopularBooksResponse,
    ActiveUsersResponse,
    SystemOverviewResponse
)
from app.core.database import get_db

router = APIRouter(prefix="/api/stats", tags=["statistics"])

@router.get("/books/popular", response_model=list[PopularBooksResponse])
def get_popular_books(limit: int = 10, db=Depends(get_db)):
    return StatsService(db).get_popular_books(limit)

@router.get("/users/active", response_model=list[ActiveUsersResponse])
def get_active_users(limit: int = 10, db=Depends(get_db)):
    return StatsService(db).get_active_users(limit)

@router.get("/overview", response_model=SystemOverviewResponse)
def get_system_overview(db=Depends(get_db)):
    return StatsService(db).get_system_overview()