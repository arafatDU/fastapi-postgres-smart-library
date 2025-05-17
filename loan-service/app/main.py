from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.init_db import create_tables
from app.api.routes.loan import router as loan_router
import os
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Application started and database tables created!")
    yield
    print("Application shutting down!")

app = FastAPI(
    title="Loan Service",
    description="Loan Service for Smart Library System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(loan_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8083))
    uvicorn.run(app, host="0.0.0.0", port=port)