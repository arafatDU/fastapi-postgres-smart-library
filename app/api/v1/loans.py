# app/api/v1/loans.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.loan import LoanService
from app.schemas.loan import LoanCreate, LoanResponse
from app.core.database import get_db

router = APIRouter(prefix="/api/loans", tags=["loans"])

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db=Depends(get_db)):
    return LoanService(db).issue_loan(loan)

@router.post("/returns")
def return_loan(loan_id: int, db=Depends(get_db)):
    return LoanService(db).return_loan(loan_id)

@router.get("/{user_id}", response_model=list[LoanResponse])
def get_user_loans(user_id: int, db=Depends(get_db)):
    return LoanService(db).get_user_loans(user_id)

@router.get("/overdue", response_model=list[LoanResponse])
def get_overdue_loans(db=Depends(get_db)):
    return LoanService(db).get_overdue_loans()

@router.put("/{loan_id}/extend", response_model=LoanResponse)
def extend_loan(loan_id: int, extension_days: int, db=Depends(get_db)):
    return LoanService(db).extend_loan(loan_id, extension_days)