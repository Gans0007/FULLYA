import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.filters import Command
from utils.ui import safe_replace_message
from db.db import database

from handlers.texts.about_me import MEMBERS_TEXTS

router = Router()
logger = logging.getLogger(__name__)

PAGE_SIZE = 5  # количество участников на одной странице


async def get_lang(user_id: int) -> str:
    row = await database.fetch_one(
        "SELECT language FROM users WHERE user_id = :uid", {"uid": user_id}
    )
    if not row:
        return "ru"
    try:
        lang = row["language"]
    except Exception:
        return "ru"
    return lang if lang in MEMBERS_TEXTS else "ru"


# ——— data access ———

async def get_participants(offset: int = 0, limit: int = PAGE_SIZE):
    """Получение участников (только видимых)"""
    logger.debug(f"[PARTICIPANTS] offset={offset}, limit={limit}")
    rows = await database.fetch_all(
        """
        SELECT user_id, username, name, age, specialization
        FROM profiles
        WHERE is_visible = TRUE
        ORDER BY user_id
        LIMIT :limit OFFSET :offset
        """,
        {"limit": limit, "offset": offset},
    )
    return [dict(row) for row in rows]


async def get_total_participant_count():
    """Общее количество участников"""
    row = await database.fetch_one(
        "SELECT COUNT(*) AS count FROM profiles WHERE is_visible = TRUE"
    )
    return row["count"] if row else 0


# ——— formatting ———

def get_user_card_text(participant: dict, T: dict):
    """
    Формирует текст карточки участника.
    «Помощь» -> profiles.help_text
    «Соц. сеть» -> profiles.message
    """
    username = (participant.get("username") or "").strip()
    name = participant.get("name") or ""
    age = participant.get("age") or T["age_not_set"]
    specialization = participant.get("specialization") or T["spec_not_set"]

    help_text = (participant.get("help_text") or "").strip() or T["help_not_set"]
    social_text = (participant.get("message") or "").strip() or T["social_not_set"]

    display_name = f"@{username}" if username else (name or T.get("name_not_set", "—"))

    return (
        f"{display_name}\n"
        f"{T['age'].format(age=age)}\n"
        f"{T['spec'].format(spec=specialization)}\n"
        f"{T['help'].format(help=help_text)}\n"
        f"{T['social'].format(social=social_text)}"
    )


async def get_participants_keyboard(participants: list[dict], page: int, T: dict):
    """Формирует клавиатуру со списком участников"""
    keyboard = []
    for participant in participants:
        user_id = participant["user_id"]
        username = participant.get("username") or ""
        name = participant.get("name") or ""
        display_name = f"@{username}" if username else (name or T.get("name_not_set", "—"))
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=display_name,
                    callback_data=f"show_card:{user_id}:{page}",
                )
            ]
        )

    total_count = await get_total_participant_count()
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text=T["nav_back"], callback_data=f"members_page:{page - 1}")
        )
    if (page + 1) * PAGE_SIZE < total_count:
        nav_buttons.append(
            InlineKeyboardButton(text=T["nav_forward"], callback_data=f"members_page:{page + 1}")
        )
    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ——— handlers ———

@router.message(Command("members"))
@router.message(F.text == "👥 Участники")
async def show_participants(msg_or_cb: Message | CallbackQuery, replace: bool = True):
    """Показывает список участников (первая страница)"""
    user_id = msg_or_cb.from_user.id
    lang = await get_lang(user_id)
    T = MEMBERS_TEXTS[lang]

    logger.info(f"[PARTICIPANTS] Пользователь {user_id} открыл список участников")
    page = 0
    participants = await get_participants(offset=page * PAGE_SIZE)
    keyboard = await get_participants_keyboard(participants, page, T)

    # Кнопка "Назад"
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=T["back_to_menu"], callback_data="back_to_about")]
    )

    text = T["participants_title"]
    if isinstance(msg_or_cb, CallbackQuery):
        await safe_replace_message(msg_or_cb.message, text=text, reply_markup=keyboard)
        await msg_or_cb.answer()
    else:
        await safe_replace_message(msg_or_cb, text=text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("members_page:"))
async def paginate_participants(callback: CallbackQuery):
    """Переключение страниц"""
    lang = await get_lang(callback.from_user.id)
    T = MEMBERS_TEXTS[lang]

    page = int(callback.data.split(":")[1])
    logger.info(f"[PARTICIPANTS] Пользователь {callback.from_user.id} перешёл на страницу {page}")
    participants = await get_participants(offset=page * PAGE_SIZE)
    keyboard = await get_participants_keyboard(participants, page, T)

    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=T["back_to_menu"], callback_data="back_to_about")]
    )

    text = T["participants_title"]
    await safe_replace_message(callback.message, text=text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("show_card:"))
async def show_user_card(callback: CallbackQuery):
    """Показывает карточку выбранного участника"""
    lang = await get_lang(callback.from_user.id)
    T = MEMBERS_TEXTS[lang]

    _, user_id, page = callback.data.split(":")
    user_id = int(user_id)
    page = int(page)
    logger.info(
        f"[PARTICIPANTS] Пользователь {callback.from_user.id} открыл карточку user_id={user_id} (стр {page})"
    )

    participant = await database.fetch_one(
        """
        SELECT user_id, username, name, age, specialization, help_text, message
        FROM profiles
        WHERE user_id = :uid AND is_visible = TRUE
        """,
        {"uid": user_id},
    )

    if not participant:
        logger.warning(f"[PARTICIPANTS] Карточка не найдена: user_id={user_id}")
        await callback.answer(T["profile_not_found"], show_alert=True)
        return

    participant = dict(participant)
    text = get_user_card_text(participant, T)

    # Кнопка «Связаться»: по Telegram-username или через tg://user?id=...
    username = (participant.get("username") or "").strip()
    contact_url = f"https://t.me/{username}" if username else f"tg://user?id={user_id}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=T["btn_contact"], url=contact_url)],
            [InlineKeyboardButton(text=T["card_back"], callback_data=f"members_page:{page}")],
        ]
    )

    await safe_replace_message(callback.message, text=text, reply_markup=kb)
    await callback.answer()
