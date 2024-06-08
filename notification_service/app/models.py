from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # Assuming there's a User model with which this links
    message: str
    type: str  # E.g., 'email', 'sms', 'push'
    status: str  # E.g., 'pending', 'sent', 'failed'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
