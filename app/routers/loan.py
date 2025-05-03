from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import controllers, schemas, database

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/loans", response_model=schemas.loan.Loan)
def issue_loan(loan: schemas.loan.LoanCreate, db: Session = Depends(get_db)):
    # TODO: check user & book exist and availability
    return controllers.loan.create_loan(db, loan)

@router.post("/returns", response_model=schemas.loan.Loan)
def return_loan(ret: schemas.loan.LoanReturn, db: Session = Depends(get_db)):
    return controllers.loan.return_loan(db, ret)

@router.get("/loans/{user_id}", response_model=list[schemas.loan.Loan])
def user_loans(user_id: int, db: Session = Depends(get_db)):
    return controllers.loan.get_loans_by_user(db, user_id)

@router.get("/loans/overdue", response_model=list[schemas.loan.Loan])
def overdue_loans(db: Session = Depends(get_db)):
    return controllers.loan.get_overdue_loans(db)

@router.put("/loans/{loan_id}/extend", response_model=schemas.loan.Loan)
def extend_loan(loan_id: int, ext: schemas.loan.LoanExtend, db: Session = Depends(get_db)):
    return controllers.loan.extend_loan(db, loan_id, ext)