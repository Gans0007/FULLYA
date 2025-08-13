import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # пример: @yourchannel
CHAT_USERNAME = os.getenv("CHAT_USERNAME")        # пример: @yourchat

public_chat_id = os.getenv("PUBLIC_CHAT_ID")
if not public_chat_id:
    raise ValueError("❌ PUBLIC_CHAT_ID не найден в .env")
PUBLIC_CHAT_ID = int(public_chat_id)
PUBLIC_CHANNEL_ID = int(os.getenv("PUBLIC_CHANNEL_ID"))

ADMIN_ID = 900410719  # Замени на свой Telegram user ID

REFERRAL_BANNER_PATH = "media/referral_banner.jpg"
REFERRAL_BASE_URL = "https://t.me/yourambitionsbot"

ADMIN_IDS = [900410719]


