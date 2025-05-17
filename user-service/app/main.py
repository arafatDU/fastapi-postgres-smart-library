from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import user as user_router
from app.database.init_db import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_tables()
    print("Application started and database tables created!")
    yield
    # Shutdown logic
    print("Application shutting down!")

app = FastAPI(
    title="User Service",
    description="User Service for Smart Library System",
    lifespan=lifespan,
)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(user_router.router)

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable or use 8081 as default
    port = int(os.getenv("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)