import os

TARGET_IMAP_HOST = os.getenv("TARGET_IMAP_HOST", "stalwart-mail")
TARGET_IMAP_PASSWORD = os.getenv("TARGET_IMAP_PASSWORD", "Fatsa2026!")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
