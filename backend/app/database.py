import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models.user_state import UserState

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://stalwart:6cfd8b77509322b29b7be96660d75346@db:5432/stalwart"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class AppConfig(Base):
    __tablename__ = "config"
    key = Column(String, primary_key=True, index=True)
    value = Column(String)

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    status = Column(String, default=UserState.NEW.value)
    mails = Column(Integer, default=0)
    size = Column(String, default="0MB")
    error = Column(String, nullable=True)
    source_password = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

class DBSession:
    def __init__(self):
        self.db = None

    def _get_db(self):
        if self.db is None:
            self.db = SessionLocal()
        return self.db

    def get_config(self, key: str, default: str = ""):
        c = self._get_db().query(AppConfig).filter(AppConfig.key == key).first()
        return c.value if c else default
    
    def set_config(self, key: str, value: str):
        db = self._get_db()
        c = db.query(AppConfig).filter(AppConfig.key == key).first()
        if c:
            c.value = value
        else:
            db.add(AppConfig(key=key, value=value))
        db.commit()

    def get_all_users(self):
        return self._get_db().query(User).all()

    def add_user(self, email: str, source_password: str = ""):
        db = self._get_db()
        u = db.query(User).filter(User.email == email).first()
        if not u:
            u = User(email=email, source_password=source_password)
            db.add(u)
        else:
            u.source_password = source_password
        db.commit()

    def update_user_state(self, email: str, state: UserState):
        db = self._get_db()
        u = db.query(User).filter(User.email == email).first()
        if u:
            u.status = state.value
            db.commit()

    def set_error(self, email: str, error: str):
        db = self._get_db()
        u = db.query(User).filter(User.email == email).first()
        if u:
            u.status = UserState.ERROR.value
            u.error = error
            db.commit()

db_session = DBSession()
