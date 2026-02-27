from fastapi import APIRouter

router = APIRouter()

@router.post("/mx_check")
def mx_check():
    # placeholder: DNS + SMTP test
    return {"result": "MX check OK"}
