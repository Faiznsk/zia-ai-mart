from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class PaymentCreate(SQLModel):
    order_id: int
    user_id: int
    amount: float
    payment_method: str
    status: str

class PaymentResponse(SQLModel):
    id: int
    order_id: int
    user_id: int
    amount: float
    payment_method: str
    status: str
    created_at: datetime
    updated_at: datetime

class PaymentUpdate(SQLModel):
    order_id: Optional[int] = None
    user_id: Optional[int] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
