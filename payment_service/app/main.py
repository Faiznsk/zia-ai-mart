from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db import create_db_and_tables, get_session

from app.schema import PaymentResponse ,PaymentCreate , PaymentUpdate
from sqlmodel import Session, select 
from app.models import Payment



# Async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables for users..")
    create_db_and_tables()  # Create database tables
    yield  # Application startup

# Create FastAPI app with custom lifespan and metadata
app = FastAPI(
    lifespan=lifespan,
    title="Payment_service_API",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8009",
            "description": "Development Server"
        }
    ]
)


# Root endpoint
@app.get("/")
def read_root():
    return {"Welcome": "payment_service"}

# CRUD operations
@app.post("/payments-management/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_session)):
    db_payment = Payment.from_orm(payment)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_session)):
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_session)):
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@app.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_session)):
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"detail": "Payment deleted successfully"}

@app.get("/payments/", response_model=List[PaymentResponse])
def get_all_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    statement = select(Payment).offset(skip).limit(limit)
    results = db.exec(statement).all()
    return results


