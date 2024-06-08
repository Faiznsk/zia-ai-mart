# Pydantic models for request and response
from typing import Optional
from sqlmodel import SQLModel


class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True

