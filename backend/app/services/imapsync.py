import subprocess
from app.database import db_session
from app.models.user_state import UserState
from app.settings import TARGET_IMAP_HOST

def run_imapsync(user_email: str, source_pass: str, target_pass: str):
    try:
        zimbra_host = db_session.get_config("zimbra_host", "zimbra.domain.com")
        db_session.update_user_state(user_email, UserState.FULL_SYNC_RUNNING)
        cmd = [
            "imapsync",
            "--host1", zimbra_host,
            "--user1", user_email,
            "--password1", source_pass,
            "--host2", TARGET_IMAP_HOST,
            "--user2", user_email,
            "--password2", target_pass,
            "--ssl1", "--ssl2",
            "--syncinternaldates"
        ]
        subprocess.run(cmd, check=True)
        db_session.update_user_state(user_email, UserState.FULL_SYNC_DONE)
    except subprocess.CalledProcessError as e:
        db_session.set_error(user_email, str(e))
