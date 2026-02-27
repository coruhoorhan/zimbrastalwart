from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_monitoring_data():
    return {"status": "ok"}
