from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, sync, cutover, monitoring, logs, config
from app.database import init_db

app = FastAPI(title="Enterprise Mail Migration Platform")


@app.on_event("startup")
def startup_event():
    init_db()

# CORS definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(sync.router, prefix="/sync", tags=["Sync"])
app.include_router(cutover.router, prefix="/cutover", tags=["Cutover"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(config.router, prefix="/config", tags=["Config"])
