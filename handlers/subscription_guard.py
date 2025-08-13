from datetime import datetime, timedelta
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from repositories.profiles.profile_repository import get_user
from config import ADMIN_ID
from handlers.texts.notifications_texts import SUBSCRIPTION_TEXTS
from db.db import database  # чтобы взять язык

SUBSCRIPTION_DAYS = 30
TRIBUTE_PAYMENT_LINK = "https://t.me/tribute/app?startapp=ssdz"

async def has_active_subscription(user_id: int, message):
    # Если админ – всегда True
    if user_id == ADMIN_ID:
        return True

    user = await get_user(user_id)
    if not user:
        return False

    data = dict(user)
    is_paid = data.get("is_paid", False)
    payment_date = data.get("payment_date")

    if is_paid and payment_date:
        expire_date = payment_date + timedelta(days=SUBSCRIPTION_DAYS)
        if datetime.utcnow() < expire_date:
            return True

    # Получаем язык пользователя (fallback ru)
    lang_row = await database.fetch_one(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    lang = lang_row["language"] if lang_row and lang_row["language"] in SUBSCRIPTION_TEXTS else "ru"
    texts = SUBSCRIPTION_TEXTS[lang]

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=texts["pay_button"],
            url=TRIBUTE_PAYMENT_LINK
        )
    )

    await message.answer(
        texts["expired_message"],
        reply_markup=kb.as_markup()
    )
    return False
