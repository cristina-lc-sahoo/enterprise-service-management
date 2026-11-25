from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "Medium"

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "employee"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class TicketAssign(BaseModel):
    assigned_to: int
