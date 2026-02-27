from app.models.user_state import UserState
from app.workers import sync_worker


class DummyDB:
    def __init__(self):
        self.calls = []

    def get_config(self, _key, default=""):
        return "zimbra.test.local" or default

    def update_user_state(self, email, state):
        self.calls.append((email, state.value))

    def set_error(self, email, error):
        self.calls.append((email, f"ERROR:{error}"))


def test_worker_sets_full_sync_states(monkeypatch):
    dummy_db = DummyDB()
    monkeypatch.setattr(sync_worker, "db_session", dummy_db)
    monkeypatch.setattr(sync_worker.subprocess, "run", lambda *args, **kwargs: None)

    sync_worker.sync_user_mail.run("user@test.com", "src", "dst", "full")

    assert dummy_db.calls[0] == ("user@test.com", UserState.FULL_SYNC_RUNNING.value)
    assert dummy_db.calls[1] == ("user@test.com", UserState.FULL_SYNC_DONE.value)


def test_worker_sets_delta_sync_states(monkeypatch):
    dummy_db = DummyDB()
    monkeypatch.setattr(sync_worker, "db_session", dummy_db)
    monkeypatch.setattr(sync_worker.subprocess, "run", lambda *args, **kwargs: None)

    sync_worker.sync_user_mail.run("user@test.com", "src", "dst", "delta")

    assert dummy_db.calls[0] == ("user@test.com", UserState.DELTA_SYNC_RUNNING.value)
    assert dummy_db.calls[1] == ("user@test.com", UserState.DELTA_DONE.value)
