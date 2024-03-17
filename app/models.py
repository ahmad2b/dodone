from typing import  Optional
from sqlmodel import SQLModel, Field, Relationship

# Shared properties
class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None
    
# Properties to recieve via API on creation
class UserCreate(UserBase):
    password: str
    
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None
    
class UserUpdate(UserBase):
    email: str | None = None # type: ignore
    password: str | None = None

class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None
    
class UpdatePassword(SQLModel):
    current_password: str
    new_password: str
    
# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    todos: list["Todo"] = Relationship(back_populates="owner")

# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int
    
class UsersOut(SQLModel):
    data: list[UserOut]
    count: int

# Shared properties
class TodoBase(SQLModel):
    title: str 
    description: str | None = None
    
# Properties to receive on todo creation
class TodoCreate(TodoBase):
    title: str 
    description: str | None = None
    
# Properties to receive on todo update
class TodoUpdate(TodoBase):
    title: str | None = None # type: ignore
    description: str | None = None

# Database model, database table inferred from class name
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User = Relationship(back_populates="todos")
    
# Properties to return via API, id is always required
class TodoOut(TodoBase):
    id: int
    owner: UserOut
    
class TodosOut(SQLModel):
    data: list[TodoOut]
    count: int
    
# Generic message
class Message(SQLModel):
    message: str
    
# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    
# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None
    
class NewPassword(SQLModel):
    token: str
    new_password: str