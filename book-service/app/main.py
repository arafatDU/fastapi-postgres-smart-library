from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes.book import router as book_router
from app.database.init_db import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Application started and database tables created!")
    yield
    print("Application shutting down!")

app = FastAPI(
    title="Book Service",
    description="Book Service for Smart Library System",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(book_router, prefix="/api/books")


@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)