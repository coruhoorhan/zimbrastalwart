from fastapi import APIRouter
from pydantic import BaseModel
from app.database import db_session

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    source_password: str

@router.get("")
def list_users():
    users = db_session.get_all_users()
    return [
        {
            "email": u.email,
            "status": u.status,
            "mails": u.mails,
            "size": u.size,
            "error": u.error
        } for u in users
    ]

@router.post("")
def add_user(user: UserCreate):
    db_session.add_user(user.email, user.source_password)
    return {"status": "ok"}

@router.post("/import")
def import_users():
    from app.services.zimbra import fetch_users_from_zimbra
    users = fetch_users_from_zimbra()
    for email in users:
        db_session.add_user(email)
    return {"imported": len(users)}
