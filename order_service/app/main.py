from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db import create_db_and_tables, get_session
from app.models import Order , UpdateOrder
from sqlmodel import Session, select
from app.schema import OrderCreate , OrderUpdate, OrderResponse 





# Async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()  # Create database tables
    yield  # Application startup

# Create FastAPI app with custom lifespan and metadata
app = FastAPI(
    lifespan=lifespan,
    title="Order_service_API",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8008",
            "description": "Development Server"
        }
    ]
)


# Root endpoint
@app.get("/")
def read_root():
    return {"Welcome": "order_service"}

# CRUD operations
@app.post("/orders/", response_model=OrderResponse)
def create_order(order: Order, db: Session = Depends(get_session)):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_session)):
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: UpdateOrder, db: Session = Depends(get_session)):
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_session)):
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}

@app.get("/orders/", response_model=List[OrderResponse])
def get_all_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    statement = select(Order).offset(skip).limit(limit)
    results = db.exec(statement).all()
    return results
