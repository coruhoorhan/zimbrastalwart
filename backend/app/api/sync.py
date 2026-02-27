from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
from app.database import db_session
from app.models.user_state import UserState
from app.services.stalwart import create_user_on_stalwart
from app.workers.sync_worker import sync_user_mail

router = APIRouter()

class TestSyncData(BaseModel):
    zimbra_host: str
    email: str
    source_password: str

@router.post("/test")
def test_sync(data: TestSyncData):
    cmd = [
        "imapsync",
        "--host1", data.zimbra_host,
        "--user1", data.email,
        "--password1", data.source_password,
        "--host2", "stalwart-mail",
        "--user2", data.email,
        "--password2", "Fatsa2026!",
        "--ssl1", "--ssl2",
        "--justlogin"
    ]
    try:
        # We need to run this synchronously for immediate feedback
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"status": "success", "message": "Connection and dry-run login successful!"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr if e.stderr else e.stdout}

@router.post("/full")
def full_sync():
    users = db_session.get_all_users()
    for u in users:
        if u.status == UserState.NEW.value:
            create_user_on_stalwart(u.email)
            db_session.update_user_state(u.email, UserState.ACCOUNT_CREATED)
        passw = u.source_password if u.source_password else "sourcepass"
        sync_user_mail.delay(u.email, passw, "Fatsa2026!")
    return {"started": len(users)}

@router.post("/delta")
def delta_sync():
    users = db_session.get_all_users()
    for u in users:
        if u.status == UserState.FULL_SYNC_DONE.value or u.status == UserState.DONE.value:
            passw = u.source_password if u.source_password else "sourcepass"
            sync_user_mail.delay(u.email, passw, "Fatsa2026!")
    return {"started": len(users)}
