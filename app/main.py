# app/main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.users import router as users_router
from app.api.v1.books import router as books_router
from app.api.v1.loans import router as loans_router
from app.api.v1.stats import router as stats_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Library System",
    version="1.0.0",
    description="Monolithic library management system"
)

app.include_router(users_router)
app.include_router(books_router)
app.include_router(loans_router)
app.include_router(stats_router)