from celery import Celery
import subprocess
from app.models.user_state import UserState
from app.database import db_session

celery_app = Celery('worker', broker='redis://redis:6379/0')

@celery_app.task(bind=True)
def sync_user_mail(self, user_email: str, source_pass: str, target_pass: str):
    zimbra_host = db_session.get_config("zimbra_host", "zimbra.domain.com")
    try:
        cmd = [
            "imapsync",
            "--host1", zimbra_host,
            "--user1", user_email,
            "--password1", source_pass,
            "--host2", "stalwart-mail",
            "--user2", user_email,
            "--password2", target_pass,
            "--ssl1", "--ssl2",
            "--syncinternaldates",
            "--justlogin"
        ]
        # justlogin is for MVP testing fast failure/success
        subprocess.run(cmd, check=True)
        db_session.update_user_state(user_email, UserState.DONE)
    except subprocess.CalledProcessError:
        db_session.update_user_state(user_email, UserState.ERROR)
        raise
