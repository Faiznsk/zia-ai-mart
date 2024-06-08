from fastapi import Form  # Import Form for handling form data in FastAPI
from pydantic import BaseModel  # Import BaseModel from Pydantic for data validation
from sqlmodel import SQLModel, Field  # Import SQLModel and Field from SQLModel for ORM and field definitions
from typing import Annotated  # Import Annotated for type annotations

# Define a User model representing a user, inheriting from SQLModel for ORM mapping
class User (SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Primary key, auto-incremented
    username: str  # Username of the user
    email: str  # Email of the user
    password: str  # Password of the user
    phone: str 

class UpdateUser (SQLModel):
    username: str  # Username of the user
    email: str  # Email of the user
    password: str  # Password of the user
    phone: str