from sqlalchemy.orm import Session
from datetime import timedelta, datetime, UTC
from ..models.loan import Loan
from ..schemas.loan import LoanCreate, LoanReturn, LoanExtend


def get_loan(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()


def get_loans_by_user(db: Session, user_id: int):
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def get_overdue_loans(db: Session):
    now = datetime.now(UTC)
    return db.query(Loan).filter(Loan.due_date < now, Loan.status == "ACTIVE").all()


def create_loan(db: Session, loan: LoanCreate):
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def return_loan(db: Session, loan: LoanReturn):
    db_loan = get_loan(db, loan.loan_id)
    db_loan.return_date = datetime.now(UTC)
    db_loan.status = "RETURNED"
    db.commit()
    db.refresh(db_loan)
    return db_loan


def extend_loan(db: Session, loan_id: int, ext: LoanExtend):
    db_loan = get_loan(db, loan_id)
    db_loan.extensions_count += 1
    db_loan.due_date += timedelta(days=ext.extension_days)
    db_loan.status = "ACTIVE"
    db.commit()
    db.refresh(db_loan)
    return db_loan