from fastapi import APIRouter
from pydantic import BaseModel
from app.database import db_session

router = APIRouter()

class ConfigUpdate(BaseModel):
    zimbra_host: str

@router.get("")
def get_config():
    return {
        "zimbra_host": db_session.get_config("zimbra_host", "zimbra.domain.com")
    }

@router.post("")
def save_config(config: ConfigUpdate):
    db_session.set_config("zimbra_host", config.zimbra_host)
    return {"status": "success"}
