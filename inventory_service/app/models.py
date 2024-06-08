from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int  # Assuming there's a Product model with which this links
    quantity: int
    location: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
