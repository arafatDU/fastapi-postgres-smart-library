import pytest
from fastapi import status
from datetime import datetime, timedelta

class TestLoanAPI:
    def test_create_loan(self, client, test_user, test_book):
        loan_data = {
            "user_id": test_user["id"],
            "book_id": test_book["id"],
            "due_date": (datetime.now() + timedelta(days=14)).isoformat()
        }
        response = client.post("/api/loans/", json=loan_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["user_id"] == loan_data["user_id"]
        assert data["book_id"] == loan_data["book_id"]
        assert "id" in data
        assert "issue_date" in data
        assert "due_date" in data
        assert data["status"] == "ACTIVE"
    
    def test_return_loan(self, client, test_loan):
        loan_id = test_loan["id"]
        return_data = {
            "loan_id": loan_id
        }
        
        response = client.post("/api/loans/returns", json=return_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == loan_id
        assert data["status"] == "RETURNED"
        assert "return_date" in data
    
    def test_get_user_loans(self, client, test_loan):
        user_id = test_loan["user_id"]
        response = client.get(f"/api/loans/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check if test_loan is in the response
        loan_ids = [loan["id"] for loan in data]
        assert test_loan["id"] in loan_ids
    
    def test_get_overdue_loans(self, client, db_session, test_loan):
        # Modify the test_loan to make it overdue
        from app.models.loan import Loan
        loan = db_session.query(Loan).filter(Loan.id == test_loan["id"]).first()
        loan.due_date = datetime.now() - timedelta(days=1)  # Set due date to yesterday
        db_session.commit()
        
        response = client.get("/api/loans/overdue")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        
        # Check if our overdue loan is in the response
        loan_ids = [loan["id"] for loan in data]
        assert test_loan["id"] in loan_ids
    
    def test_extend_loan(self, client, test_loan):
        loan_id = test_loan["id"]
        extend_data = {
            "extension_days": 7  # Extend by 7 days
        }
        
        response = client.put(f"/api/loans/{loan_id}/extend", json=extend_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == loan_id
        
        # The due_date should be updated (7 days later than the original due date)
        original_due_date = datetime.fromisoformat(test_loan["due_date"])
        new_due_date = datetime.fromisoformat(data["due_date"])
        assert (new_due_date - original_due_date).days == 7
    
    def test_multiple_loans_and_available_count(self, client, test_user, test_book):
        # First loan already exists from the test_loan fixture
        # Try to make another loan for the same book
        loan_data = {
            "user_id": test_user["id"],
            "book_id": test_book["id"],
            "due_date": (datetime.now() + timedelta(days=14)).isoformat()
        }
        
        # Get the book to check available count before making another loan
        response = client.get(f"/api/books/{test_book['id']}")
        book_before = response.json()
        
        # Make another loan
        response = client.post("/api/loans/", json=loan_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the available count has decreased
        response = client.get(f"/api/books/{test_book['id']}")
        book_after = response.json()
        
        assert book_after["available_copies"] == book_before["available_copies"] - 1
