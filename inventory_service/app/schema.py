from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class InventoryCreate(SQLModel):
    product_id: int
    quantity: int
    location: Optional[str] = None

class InventoryResponse(SQLModel):
    id: int
    product_id: int
    quantity: int
    location: Optional[str] = None
    last_updated: datetime

class InventoryUpdate(SQLModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
