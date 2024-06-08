from datetime import datetime  # Correct import
from fastapi import Form  # Import Form for handling form data in FastAPI
from pydantic import BaseModel  # Import BaseModel from Pydantic for data validation
from sqlmodel import SQLModel, Field  # Import SQLModel and Field from SQLModel for ORM and field definitions
from typing import Annotated, Optional  # Import Annotated for type annotations

# Order model using SQLModel
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    user_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Order model using SQLModel
class UpdateOrder(SQLModel):
    
    product_id: int
    user_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)