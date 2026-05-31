import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = []

if ADMIN_IDS_RAW:
    ADMIN_IDS = [
        int(admin_id.strip())
        for admin_id in ADMIN_IDS_RAW.split(",")
        if admin_id.strip().isdigit()
    ]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")
