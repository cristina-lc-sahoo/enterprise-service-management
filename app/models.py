from sqlalchemy.sql import func
from .database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="Open")
    priority = Column(String(20), default="Medium")
    created_at = Column(DateTime, server_default=func.now())
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), default="employee")
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
