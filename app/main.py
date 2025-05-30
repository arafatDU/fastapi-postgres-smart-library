from fastapi import FastAPI
from .database import engine, Base
from .routers import user, book, loan

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Library System")


app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(book.router, prefix="/api/books", tags=["Books"])
app.include_router(loan.router, prefix="/api/loans", tags=["Loans"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart Library System!"}