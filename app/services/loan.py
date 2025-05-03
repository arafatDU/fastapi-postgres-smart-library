from datetime import datetime, timedelta
from fastapi import HTTPException
from app.repositories.loan import LoanRepository
from app.repositories.book import BookRepository
from app.schemas.loan import LoanCreate, LoanResponse

class LoanService:
    def __init__(self, db):
        self.loan_repo = LoanRepository(db)
        self.book_repo = BookRepository(db)
        self.user_repo = UserRepository(db)

    def issue_loan(self, loan_data: LoanCreate):
        # Check user exists
        if not self.user_repo.get_user(loan_data.user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check book availability
        book = self.book_repo.get_book(loan_data.book_id)
        if not book or book.available_copies < 1:
            raise HTTPException(status_code=400, detail="Book not available")
        
        # Update book copies
        book.available_copies -= 1
        self.book_repo.update_book(book)
        
        # Create loan
        return self.loan_repo.create_loan(loan_data)

    def return_loan(self, loan_id: int):
        loan = self.loan_repo.get_loan(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        
        # Update loan status
        loan.status = "RETURNED"
        loan.return_date = datetime.utcnow()
        
        # Update book availability
        book = self.book_repo.get_book(loan.book_id)
        book.available_copies += 1
        self.book_repo.update_book(book)
        
        self.loan_repo.update_loan(loan)
        return loan