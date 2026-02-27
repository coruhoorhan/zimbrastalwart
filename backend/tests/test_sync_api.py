from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import sync


class DummyTask:
    def __init__(self):
        self.calls = []

    def delay(self, *args):
        self.calls.append(args)


class DummyDB:
    def __init__(self, users):
        self.users = users
        self.state_updates = []

    def get_all_users(self):
        return self.users

    def update_user_state(self, email, state):
        self.state_updates.append((email, state.value))


def test_full_sync_queues_only_eligible_users(monkeypatch):
    users = [
        SimpleNamespace(email="new@x.com", status="NEW", source_password="p1"),
        SimpleNamespace(email="created@x.com", status="ACCOUNT_CREATED", source_password="p2"),
        SimpleNamespace(email="done@x.com", status="FULL_SYNC_DONE", source_password="p3"),
    ]
    dummy_db = DummyDB(users)
    task = DummyTask()

    monkeypatch.setattr(sync, "db_session", dummy_db)
    monkeypatch.setattr(sync, "sync_user_mail", task)
    monkeypatch.setattr(sync, "create_user_on_stalwart", lambda _email: True)

    app = FastAPI()
    app.include_router(sync.router, prefix="/sync")
    client = TestClient(app)

    response = client.post("/sync/full")
    assert response.status_code == 200
    assert response.json()["started"] == 2
    assert task.calls == [
        ("new@x.com", "p1", sync.TARGET_IMAP_PASSWORD, "full"),
        ("created@x.com", "p2", sync.TARGET_IMAP_PASSWORD, "full"),
    ]


def test_delta_sync_queues_only_completed_users(monkeypatch):
    users = [
        SimpleNamespace(email="full@x.com", status="FULL_SYNC_DONE", source_password="p1"),
        SimpleNamespace(email="delta@x.com", status="DELTA_DONE", source_password="p2"),
        SimpleNamespace(email="new@x.com", status="NEW", source_password="p3"),
    ]
    dummy_db = DummyDB(users)
    task = DummyTask()

    monkeypatch.setattr(sync, "db_session", dummy_db)
    monkeypatch.setattr(sync, "sync_user_mail", task)

    app = FastAPI()
    app.include_router(sync.router, prefix="/sync")
    client = TestClient(app)

    response = client.post("/sync/delta")
    assert response.status_code == 200
    assert response.json()["started"] == 2
    assert task.calls == [
        ("full@x.com", "p1", sync.TARGET_IMAP_PASSWORD, "delta"),
        ("delta@x.com", "p2", sync.TARGET_IMAP_PASSWORD, "delta"),
    ]
