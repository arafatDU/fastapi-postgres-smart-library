from fastapi import FastAPI
from .database import engine, Base



app = FastAPI(title="Smart Library System")


@app.get("/")
async def root():
    return {"message": "Welcome to the Smart Library System!"}