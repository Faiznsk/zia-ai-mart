from sqlmodel import SQLModel


class UserBase (SQLModel):
    username: str  # Username of the user
    email: str  # Email of the user
    password: str  # Password of the user
    phone: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id:int

    class Config:
        orm_mode = True


