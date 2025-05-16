import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app import database

# Test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    # Dependency override
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[database.get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(client, db_session):
    import uuid
    unique_email = f"test-{uuid.uuid4()}@example.com"
    
    user_data = {
        "name": f"Test User {uuid.uuid4().hex[:8]}",
        "email": unique_email,
        "role": "user"
    }
    response = client.post("/api/users/", json=user_data)
    if response.status_code == 400 and "Email already registered" in response.text:
        # Try with a different email
        unique_email = f"test-{uuid.uuid4()}@example.com"
        user_data["email"] = unique_email
        response = client.post("/api/users/", json=user_data)
    
    assert response.status_code == 200, f"Failed to create test user: {response.text}"
    return response.json()

@pytest.fixture(scope="function")
def test_book(client, db_session):
    import uuid
    
    # Generate a unique ISBN for each test
    unique_isbn = str(uuid.uuid4())[:13]
    
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": unique_isbn,
        "copies": 5,
        "available_copies": 5
    }
    response = client.post("/api/books/", json=book_data)
    assert response.status_code == 200
    return response.json()
    return response.json()

@pytest.fixture(scope="function")
def test_loan(client, test_user, test_book):
    from datetime import datetime, timedelta
    
    loan_data = {
        "user_id": test_user["id"],
        "book_id": test_book["id"],
        "due_date": (datetime.now() + timedelta(days=14)).isoformat()
    }
    # Print for debugging
    print(f"Creating test loan with data: {loan_data}")
    response = client.post("/api/loans/", json=loan_data)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 200, f"Failed to create test loan: {response.text}"
    return response.json()
