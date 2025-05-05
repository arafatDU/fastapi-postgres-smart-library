from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import services, schemas, database
from ..exceptions import ResourceNotFoundException

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
    
    user = services.user.get_user(db, loan.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    book = services.book.get_book(db, loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    try:
        services.book.decrease_available_book(db, loan.book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_loan = services.loan.create_loan(db, loan)
    return db_loan


@router.post("/returns", response_model=schemas.loan.Loan)
def return_loan(ret: schemas.loan.LoanReturn, db: Session = Depends(get_db)):
    db_loan = services.loan.get_loan(db, ret.loan_id)
    if not db_loan:
        raise ResourceNotFoundException(detail="Loan not found")
    try:
        services.book.increase_available_book(db, db_loan.book_id)  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return services.loan.return_loan(db, ret)


@router.get("/loans/{user_id}", response_model=list[schemas.loan.Loan])
def user_loans(user_id: int, db: Session = Depends(get_db)):
    return services.loan.get_loans_by_user(db, user_id)


@router.get("/loans/overdue", response_model=list[schemas.loan.Loan])
def overdue_loans(db: Session = Depends(get_db)):
    return services.loan.get_overdue_loans(db)


@router.put("/loans/{loan_id}/extend", response_model=schemas.loan.Loan)
def extend_loan(loan_id: int, ext: schemas.loan.LoanExtend, db: Session = Depends(get_db)):
    db_loan = services.loan.get_loan(db, loan_id)
    if not db_loan:
        raise ResourceNotFoundException(detail="Loan not found")
    return services.loan.extend_loan(db, loan_id, ext)