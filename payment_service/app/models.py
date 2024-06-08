from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int  # Assuming there's an Order model with which this links
    user_id: int  # Assuming there's a User model with which this links
    amount: float
    payment_method: str  # E.g., 'credit_card', 'paypal', etc.
    status: str  # E.g., 'pending', 'completed', 'failed'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)