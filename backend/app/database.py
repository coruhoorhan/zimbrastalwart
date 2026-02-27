from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models.user_state import UserState

# We use the postgres connection settings from your docker-compose.yml
DATABASE_URL = "postgresql://stalwart:6cfd8b77509322b29b7be96660d75346@db:5432/stalwart"

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

Base.metadata.create_all(bind=engine)

class DBSession:
    def get_config(self, key: str, default: str = ""):
        with SessionLocal() as db:
            c = db.query(AppConfig).filter(AppConfig.key == key).first()
            return c.value if c else default
    
    def set_config(self, key: str, value: str):
        with SessionLocal() as db:
            c = db.query(AppConfig).filter(AppConfig.key == key).first()
            if c:
                c.value = value
            else:
                db.add(AppConfig(key=key, value=value))
            db.commit()

    def get_all_users(self):
        with SessionLocal() as db:
            # We copy data into dicts/lists to avoid DetachedInstanceError since session closes
            users = db.query(User).all()
            db.expunge_all()
            return users

    def add_user(self, email: str, source_password: str = ""):
        with SessionLocal() as db:
            u = db.query(User).filter(User.email == email).first()
            if not u:
                u = User(email=email, source_password=source_password)
                db.add(u)
            else:
                u.source_password = source_password
            db.commit()

    def update_user_state(self, email: str, state: UserState):
        with SessionLocal() as db:
            u = db.query(User).filter(User.email == email).first()
            if u:
                u.status = state.value
                db.commit()

    def set_error(self, email: str, error: str):
        with SessionLocal() as db:
            u = db.query(User).filter(User.email == email).first()
            if u:
                u.status = UserState.ERROR.value
                u.error = error
                db.commit()

db_session = DBSession()
