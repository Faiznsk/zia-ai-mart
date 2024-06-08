from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db import create_db_and_tables, get_session

from app.schema import NotificationResponse, NotificationCreate, NotificationUpdate
from sqlmodel import Session, select

from app.models import Notification



# Async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()  # Create database tables
    yield  # Application startup

# Create FastAPI app with custom lifespan and metadata
app = FastAPI(
    lifespan=lifespan,
    title="Notification_service_API",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8010",
            "description": "Development Server"
        }
    ]
)


# Root endpoint
@app.get("/")
def read_root():
    return {"Welcome": "notification_service"}

# CRUD operations
@app.post("/notifications/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_session)):
    db_notification = Notification.from_orm(notification)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@app.get("/notifications/{notification_id}", response_model=NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_session)):
    notification = db.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.put("/notifications/{notification_id}", response_model=NotificationResponse)
def update_notification(notification_id: int, notification_update: NotificationUpdate, db: Session = Depends(get_session)):
    notification = db.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in notification_update.dict(exclude_unset=True).items():
        setattr(notification, key, value)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

@app.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_session)):
    notification = db.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return {"detail": "Notification deleted successfully"}

@app.get("/notifications/", response_model=List[NotificationResponse])
def get_all_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    statement = select(Notification).offset(skip).limit(limit)
    results = db.exec(statement).all()
    return results


