import logging
import config
from aiogram import Bot, types, Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from db.db import database

from services.confirmations.confirmation_service import was_confirmed_today
from repositories.habits.habit_repo import (
    get_habits_by_user,
    should_show_delete_button,
    count_user_habits
)
from services.challenge_service.complete_challenge import complete_challenge
from config import ADMIN_ID
from handlers.about_me.about_menu import get_about_inline_menu
from services.profile.profile_service import get_user_profile_summary
from handlers.subscription_guard import has_active_subscription
from handlers.honor_handler import show_top10_async
from handlers.texts.menu_texts import MAIN_MENU_TEXTS, MAIN_MENU_BUTTONS, MENU_TEXTS

logger = logging.getLogger(__name__)
router = Router()



async def get_lang(user_id: int) -> str:
    lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    return lang if lang in MAIN_MENU_TEXTS else "ru"



def get_main_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    t = MAIN_MENU_TEXTS.get(lang, MAIN_MENU_TEXTS["ru"])
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["add"]), KeyboardButton(text=t["active"])],
            [KeyboardButton(text=t["hall"]), KeyboardButton(text=t["dreams"])],
            [KeyboardButton(text=t["motivation"]), KeyboardButton(text=t["about"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder=t["placeholder"]
    )



@router.message(lambda msg: msg.text in [t["add"] for t in MAIN_MENU_TEXTS.values()])
async def handle_add_habit(message: types.Message):
    user_id = message.from_user.id
    if not await has_active_subscription(user_id, message):
        logger.info(f"[{user_id}] ❌ Нет активной подписки при попытке открыть меню добавления.")
        return

    lang = await get_lang(user_id)
    t_buttons = MAIN_MENU_BUTTONS[lang]
    t_menu = MENU_TEXTS[lang]

    total = await count_user_habits(user_id)
    logger.info(f"[{user_id}] 🔧 Открытие меню добавления привычки/челленджа ({total}/10 активных).")

    text = t_menu["add_description"] + f"{total}/10"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t_buttons["add_habit"], callback_data="add_habit_custom")],
        [InlineKeyboardButton(text=t_buttons["take_from_list"], callback_data="take_challenge")]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")



@router.message(lambda msg: msg.text in [t["active"] for t in MAIN_MENU_TEXTS.values()])
async def show_active_tasks(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    if not await has_active_subscription(user_id, message):
        logger.info(f"[{user_id}] ❌ Нет подписки при попытке открыть активные привычки.")
        return

    lang = await get_lang(user_id)
    t_menu = MENU_TEXTS[lang]
    t_buttons = MAIN_MENU_BUTTONS[lang]

    habits = await get_habits_by_user(user_id)
    if not habits:
        logger.info(f"[{user_id}] ℹ️ У пользователя нет активных привычек.")
        await message.answer(t_menu["no_tasks"])
        return

    logger.info(f"[{user_id}] 📋 Открытие списка активных привычек/челленджей: {len(habits)} шт.")

    for habit in habits:
        habit_id = habit.id
        name = habit.name
        days = habit.days
        description = habit.description
        done_days = habit.done_days
        is_challenge = habit.is_challenge
        confirm_type = habit.confirm_type

        if is_challenge and done_days >= days:
            logger.info(f"[{user_id}] ✅ Челлендж завершён: {name} (id: {habit_id})")
            await complete_challenge(habit_id, user_id, bot)
            continue

        title = t_menu["active_challenge_title"] if is_challenge else t_menu["active_habit_title"]
        percent = round((done_days / days) * 100) if days > 0 else 0

        text = title + "\n\n" + t_menu["active_item_text"].format(
            name=name,
            desc=description,
            done=done_days,
            total=days,
            percent=percent
        )

        buttons = []
        if not is_challenge and done_days == days:
            buttons = [
                InlineKeyboardButton(text=t_buttons["btn_complete"], callback_data=f"complete_habit_{habit_id}"),
                InlineKeyboardButton(text=t_buttons["btn_extend"], callback_data=f"extend_habit_{habit_id}")
            ]
        else:
            if confirm_type == "wake_time":
                btn_text = t_buttons["btn_wake_time"]
            elif await was_confirmed_today(user_id, habit_id):
                btn_text = t_buttons["btn_reconfirm"]
            else:
                btn_text = t_buttons["btn_confirm"]

            buttons.append(
                InlineKeyboardButton(text=btn_text, callback_data=f"confirm_done_{habit_id}")
            )

            if await should_show_delete_button(user_id, habit_id):
                buttons.append(
                    InlineKeyboardButton(text=t_buttons["btn_delete"], callback_data=f"delete_habit_{habit_id}")
                )

        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[buttons])
        )



@router.message(lambda msg: msg.text in [t["about"] for t in MAIN_MENU_TEXTS.values()])
async def show_about(message: types.Message):
    user_id = message.from_user.id
    if not await has_active_subscription(user_id, message):
        logger.info(f"[{user_id}] ❌ Нет подписки при попытке открыть раздел 'Обо мне'.")
        return

    lang = await get_lang(user_id)
    t_menu = MENU_TEXTS[lang]
    usdt, xp, liga, quote = await get_user_profile_summary(user_id)

    logger.info(f"[{user_id}] 👤 Открыл раздел 'Обо мне'. Профиль: USDT={usdt}, XP={xp}, Лига={liga}")

    text = t_menu["profile_summary"].format(usdt=usdt, xp=xp, liga=liga, quote=quote)

    await message.answer(
        text,
        reply_markup=await get_about_inline_menu(user_id)
    )



@router.message(lambda msg: msg.text in [t["hall"] for t in MAIN_MENU_TEXTS.values()])
async def handle_honor_board(message: types.Message):
    user_id = message.from_user.id
    if not await has_active_subscription(user_id, message):
        logger.info(f"[{user_id}] ❌ Нет подписки при попытке открыть Доску Почёта.")
        return

    logger.info(f"[{user_id}] 🏆 Открыл Доску Почёта")
    await show_top10_async(message)