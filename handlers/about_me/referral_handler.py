# handlers/about_me/referral_handler.py

from aiogram import Router, types, F, Bot
from config import REFERRAL_BANNER_PATH, REFERRAL_BASE_URL
from handlers.about_me.about_menu import get_about_inline_menu
from services.profile.profile_service import get_user_profile_summary
from db.db import database
from handlers.texts.about_me import REFERRAL_TEXTS

router = Router()


# --- helpers -----------------------------------------------------------------

async def get_user_lang(user_id: int) -> str:
    row = await database.fetch_one(
        "SELECT language FROM users WHERE user_id = :user_id",
        {"user_id": user_id},
    )
    lang = (row["language"] if row and row["language"] else "ru").lower()
    return lang if lang in REFERRAL_TEXTS else "ru"


def T(lang: str) -> dict:
    return REFERRAL_TEXTS.get(lang, REFERRAL_TEXTS["ru"])


# --- handlers ----------------------------------------------------------------

@router.callback_query(F.data == "about_referrals")
async def show_referral_info(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    t = T(lang)

    # Список приглашённых
    referrals = await database.fetch_all(
        """
        SELECT invited_id
        FROM referrals
        WHERE referrer_id = :referrer_id
        """,
        {"referrer_id": user_id},
    )
    invited_ids = [row["invited_id"] for row in referrals]
    total_referrals = len(invited_ids)

    # Кто оплатил (is_paid = TRUE)
    if invited_ids:
        rows = await database.fetch_all(
            """
            SELECT user_id
            FROM users
            WHERE user_id = ANY(:ids) AND is_paid = TRUE
            """,
            {"ids": invited_ids},
        )
        active_ids = {row["user_id"] for row in rows}
    else:
        active_ids = set()

    active_referrals = len(active_ids)

    # Список активных друзей
    active_friends_lines = []
    for invited_id in invited_ids:
        if invited_id in active_ids:
            try:
                user = await bot.get_chat(invited_id)
                if user.username:
                    active_friends_lines.append(
                        t["active_friend_item_with_username"].format(
                            name=user.full_name, username=user.username
                        )
                    )
                else:
                    active_friends_lines.append(
                        t["active_friend_item"].format(name=user.full_name)
                    )
            except Exception:
                active_friends_lines.append(
                    t["unknown_friend"].format(id=invited_id)
                )

    # Реф ссылка
    referral_link = f"{REFERRAL_BASE_URL}?start={user_id}"

    # Баланс USDT
    row = await database.fetch_one(
        "SELECT usdt_balance FROM users WHERE user_id = :user_id",
        {"user_id": user_id},
    )
    usdt_earned = float(row["usdt_balance"]) if row and row["usdt_balance"] is not None else 0.0

    # Выведено
    withdrawn_row = await database.fetch_one(
        "SELECT withdrawn FROM users WHERE user_id = :user_id",
        {"user_id": user_id},
    )
    withdrawn = float(withdrawn_row["withdrawn"]) if withdrawn_row and withdrawn_row["withdrawn"] is not None else 0.0

    # Сообщение
    caption_parts = [
        t["program_title"],
        t["link"].format(referral_link=referral_link),
        t["total_invited"].format(total=total_referrals),
        t["active_paid"].format(active=active_referrals),
        t["balance"].format(usdt=usdt_earned),
        t["withdrawn"].format(withdrawn=withdrawn),
    ]
    caption = "".join(caption_parts)

    if active_friends_lines:
        caption += "\n\n" + t["active_friends_title"] + "\n" + "\n".join(active_friends_lines)

    # Клавиатура
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=t["btn_withdraw"], url="https://t.me/ssprvz01"),
                types.InlineKeyboardButton(text=t["btn_rules"], callback_data="ref_rules"),
            ],
            [types.InlineKeyboardButton(text=t["btn_back"], callback_data="about_back")],
        ]
    )

    await callback.message.answer_photo(
        photo=types.FSInputFile(REFERRAL_BANNER_PATH),
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "about_back")
async def back_to_about(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    usdt, xp, liga, quote = await get_user_profile_summary(user_id)
    text = f"USDT: {usdt:.2f} | XP: {xp} | Лига: {liga}\n\n«{quote}»"

    reply_markup = await get_about_inline_menu(user_id)
    await callback.message.answer(text, reply_markup=reply_markup)


@router.callback_query(F.data == "ref_rules")
async def show_referral_rules(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    t = T(lang)

    text = (
        t["rules_title"]
        + t["rules_who_title"] + t["rules_who_text"]
        + t["rules_active_title"] + t["rules_active_text"]
        + t["rules_reward_title"] + t["rules_reward_text"]
        + t["rules_accrual_title"] + t["rules_accrual_text"]
        + t["rules_withdraw_title"] + t["rules_withdraw_text"]
    )

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()
