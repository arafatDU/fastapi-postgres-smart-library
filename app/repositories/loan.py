from sqlalchemy.orm import Session
from datetime import datetime
from app.models.loan import Loan
from app.schemas.loan import LoanCreate

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_loan(self, loan: LoanCreate) -> Loan:
        db_loan = Loan(**loan.dict())
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan

    def get_loan(self, loan_id: int) -> Loan:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def update_loan(self, loan: Loan) -> Loan:
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def get_user_loans(self, user_id: int) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.user_id == user_id).all()

    def get_overdue_loans(self) -> list[Loan]:
        return self.db.query(Loan).filter(
            Loan.due_date < datetime.utcnow(),
            Loan.status == "ACTIVE"
        ).all()