from celery import Celery
import subprocess
from app.models.user_state import UserState
from app.database import db_session
from app.settings import REDIS_URL, TARGET_IMAP_HOST

celery_app = Celery('worker', broker=REDIS_URL)

@celery_app.task(bind=True)
def sync_user_mail(self, user_email: str, source_pass: str, target_pass: str, sync_mode: str = "full"):
    zimbra_host = db_session.get_config("zimbra_host", "zimbra.domain.com")
    try:
        running_state = UserState.FULL_SYNC_RUNNING if sync_mode == "full" else UserState.DELTA_SYNC_RUNNING
        done_state = UserState.FULL_SYNC_DONE if sync_mode == "full" else UserState.DELTA_DONE
        db_session.update_user_state(user_email, running_state)

        cmd = [
            "imapsync",
            "--host1", zimbra_host,
            "--user1", user_email,
            "--password1", source_pass,
            "--host2", TARGET_IMAP_HOST,
            "--user2", user_email,
            "--password2", target_pass,
            "--ssl1", "--ssl2",
            "--syncinternaldates",
        ]
        subprocess.run(cmd, check=True)
        db_session.update_user_state(user_email, done_state)
    except subprocess.CalledProcessError as error:
        db_session.set_error(user_email, str(error))
        raise
