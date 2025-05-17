from fastapi import FastAPI
from app.api.routes import user as user_router
from app.database.init_db import create_tables

app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(user_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)