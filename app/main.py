#import libraries and dependencies

from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Ticket, User
from .schemas import TicketCreate, TicketUpdate, UserCreate, UserUpdate, TicketAssign

from pwdlib import PasswordHash

#Rehashed password

password_hash = PasswordHash.recommended()

#Initialize the FastAPI application and define its metadata

app = FastAPI(
    title="Enterprise Service Management API",
    description="API for managing enterprise support tickets",
    version="1.0.0"
)

#Provide a database session for each request and close it afterward

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#GET

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        return {"error": "Ticket not found"}

    return ticket

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}/tickets")
def get_engineer_tickets(
    user_id: int,
    db: Session = Depends(get_db)
):
    engineer = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not engineer:
        return {"error": "User not found"}

    tickets = db.query(Ticket).filter(
        Ticket.assigned_to == user_id
    ).all()

    return tickets

#POST

@app.post("/tickets")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        email=user.email,
        role=user.role,
        password_hash=password_hash.hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "user_id": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }

#PATCH

@app.patch("/tickets/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db)
):
    existing_ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not existing_ticket:
        return {"error": "Ticket not found"}

    if ticket.status is not None:
        existing_ticket.status = ticket.status

    if ticket.priority is not None:
        existing_ticket.priority = ticket.priority

    db.commit()
    db.refresh(existing_ticket)

    return existing_ticket

@app.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not existing_user:
        return {"error": "User not found"}

    if user.username is not None:
        existing_user.username = user.username

    if user.email is not None:
        existing_user.email = user.email

    if user.role is not None:
        existing_user.role = user.role

    db.commit()
    db.refresh(existing_user)

    return existing_user

@app.patch("/tickets/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    assignment: TicketAssign,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        return {"error": "Ticket not found"}

    engineer = db.query(User).filter(
        User.user_id == assignment.assigned_to
    ).first()

    if not engineer:
        return {"error": "User not found"}

    if engineer.role != "support":
        return {"error": "User is not a support engineer"}

    ticket.assigned_to = engineer.user_id

    db.commit()
    db.refresh(ticket)

    return ticket

#DELETE

@app.delete("/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        return {"error": "Ticket not found"}

    db.delete(ticket)
    db.commit()

    return {"message": f"Ticket {ticket_id} deleted successfully"}
