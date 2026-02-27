from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
from app.database import db_session
from app.models.user_state import UserState
from app.services.stalwart import create_user_on_stalwart
from app.workers.sync_worker import sync_user_mail
from app.settings import TARGET_IMAP_HOST, TARGET_IMAP_PASSWORD

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
        "--host2", TARGET_IMAP_HOST,
        "--user2", data.email,
        "--password2", TARGET_IMAP_PASSWORD,
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
    started = 0
    for u in users:
        if u.status == UserState.NEW.value:
            create_user_on_stalwart(u.email)
            db_session.update_user_state(u.email, UserState.ACCOUNT_CREATED)
        if u.status in {UserState.NEW.value, UserState.ACCOUNT_CREATED.value, UserState.ERROR.value}:
            passw = u.source_password if u.source_password else "sourcepass"
            sync_user_mail.delay(u.email, passw, TARGET_IMAP_PASSWORD, "full")
            started += 1
    return {"started": started}

@router.post("/delta")
def delta_sync():
    users = db_session.get_all_users()
    started = 0
    for u in users:
        if u.status in {UserState.FULL_SYNC_DONE.value, UserState.DELTA_DONE.value}:
            passw = u.source_password if u.source_password else "sourcepass"
            sync_user_mail.delay(u.email, passw, TARGET_IMAP_PASSWORD, "delta")
            started += 1
    return {"started": started}
