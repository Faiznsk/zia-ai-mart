from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db import create_db_and_tables, get_session

from app.schema import InventoryResponse, InventoryCreate, InventoryUpdate
from sqlmodel import Session, select

from app.models import Inventory



# Async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()  # Create database tables
    yield  # Application startup

# Create FastAPI app with custom lifespan and metadata
app = FastAPI(
    lifespan=lifespan,
    title="Inventory_service_API",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8011",
            "description": "Development Server"
        }
    ]
)


# Root endpoint
@app.get("/")
def read_root():
    return {"Welcome": "inventory_service"}

# CRUD operations
@app.post("/inventories/", response_model=InventoryResponse)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_session)):
    db_inventory = Inventory.from_orm(inventory)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@app.get("/inventories/{inventory_id}", response_model=InventoryResponse)
def read_inventory(inventory_id: int, db: Session = Depends(get_session)):
    inventory = db.get(Inventory, inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.put("/inventories/{inventory_id}", response_model=InventoryResponse)
def update_inventory(inventory_id: int, inventory_update: InventoryUpdate, db: Session = Depends(get_session)):
    inventory = db.get(Inventory, inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    for key, value in inventory_update.dict(exclude_unset=True).items():
        setattr(inventory, key, value)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

@app.delete("/inventories/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(inventory_id: int, db: Session = Depends(get_session)):
    inventory = db.get(Inventory, inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    db.delete(inventory)
    db.commit()
    return {"detail": "Inventory deleted successfully"}

@app.get("/inventories/", response_model=List[InventoryResponse])
def get_all_inventories(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    statement = select(Inventory).offset(skip).limit(limit)
    results = db.exec(statement).all()
    return results


