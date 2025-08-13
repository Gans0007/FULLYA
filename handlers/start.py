import logging
from datetime import datetime, timedelta
from aiogram import F

from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID

from keyboards.menu import get_main_menu
from handlers.texts.start_texts import (
    START_PAY_BUTTON,
    START_PAY_CAPTION,
    START_PAY_FALLBACK,
    START_NO_ACCESS,
    START_NO_ACCESS_ALERT,
    START_CHECKING,
    START_INSTRUCTION_TEXT,
    START_VIDEO_INSTRUCTION_TEXT,
    # ↓↓↓ тексты пользовательского соглашения ↓↓↓
    TERMS_TITLE,
    TERMS_TEXT,
    TERMS_ACCEPT_BTN,
)
from repositories.profiles.profile_repository import save_user, get_user, set_terms_accepted
from repositories.referrals.referral_repo import save_referral

router = Router()
logger = logging.getLogger(__name__)

SUBSCRIPTION_DAYS = 30
TRIBUTE_PAYMENT_LINK = "https://t.me/tribute/app?startapp=ssdz"

# --- commands setup (slash menu) ---
async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запустить бота"),
            # сюда добавишь и другие команды при необходимости
        ],
        scope=BotCommandScopeAllPrivateChats()
    )

# регистрируем запуск
router.startup.register(setup_bot_commands)


def _get_lang(user_row) -> str:
    """Язык из БД (поле language) с фолбэком на ru."""
    try:
        return (dict(user_row).get("language") or "ru").lower()
    except Exception:
        return "ru"


def _t(dct: dict, lang: str) -> str:
    """Достаём строку по языку с безопасным фолбэком."""
    return dct.get(lang) or dct.get("ru") or next(iter(dct.values()), "")


@router.message(F.chat.type == "private", Command("start"))
async def start_cmd(message: types.Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"[START] Пользователь {user_id} начал работу")

    # Получаем пользователя из базы
    user = await get_user(user_id)

    # Если пользователя нет в базе — создаём его
    if user is None:
        full_name = message.from_user.full_name or "-"
        await save_user(user_id, full_name)
        logger.info(f"[START] Новый пользователь {user_id} сохранён в БД")

        # Если есть параметр реферала — проверяем и сохраняем
        if message.text and len(parts := message.text.split()) == 2 and parts[1].isdigit():
            referrer_id = int(parts[1])
            if referrer_id != user_id:
                referrer = await get_user(referrer_id)
                if referrer:
                    try:
                        await save_referral(referrer_id, user_id, bot)
                        logger.info(f"[REFERRAL] Сразу сохранили реферала {referrer_id} → {user_id}")

                        # ✅ Начисляем XP пригласившему
                        from services.profile.xp_service import xp_for_referral
                        await xp_for_referral(referrer_id, bot)
                        logger.info(f"[XP] Начислен 1 XP за приглашение пользователю {referrer_id}")
                    except Exception as e:
                        logger.warning(f"[REFERRAL] Ошибка при сохранении реферала: {e}")
                else:
                    logger.warning(f"[REFERRAL] Referrer {referrer_id} не найден в users — не сохраняем")

        # Обновляем user после возможной регистрации
        user = await get_user(user_id)

    # Язык пользователя
    lang = _get_lang(user)

    # Проверка доступа по БД
    has_access = False
    if user_id == ADMIN_ID:
        has_access = True
    elif user:
        user_data = dict(user)
        is_paid = user_data.get("is_paid", False)
        payment_date = user_data.get("payment_date")
        if is_paid and payment_date:
            expire_date = payment_date + timedelta(days=SUBSCRIPTION_DAYS)
            if datetime.utcnow() < expire_date:
                has_access = True

    # Если доступа нет – только кнопка оплаты
    if not has_access:
        keyboard = InlineKeyboardBuilder()
        keyboard.row(
            types.InlineKeyboardButton(
                text=_t(START_PAY_BUTTON, lang),
                url=TRIBUTE_PAYMENT_LINK,
            )
        )
        try:
            await message.answer_photo(
                photo=FSInputFile("media/preview.jpg"),
                caption=_t(START_PAY_CAPTION, lang),
                reply_markup=keyboard.as_markup(),
            )
        except Exception as e:
            logger.critical(f"[START] Не удалось отправить стартовое фото пользователю {user_id}: {e}")
            await message.answer(
                _t(START_PAY_FALLBACK, lang),
                reply_markup=keyboard.as_markup(),
            )
        return

    # --- ДОБАВЛЕНО: если соглашение ещё не принято — показываем первым ---
    user_data = dict(user or {})
    if not user_data.get("terms_accepted", False):
        terms_kb = InlineKeyboardBuilder()
        terms_kb.row(
            types.InlineKeyboardButton(
                text=_t(TERMS_ACCEPT_BTN, lang),
                callback_data="accept_terms"
            )
        )
        await message.answer(
            text=f"<b>{_t(TERMS_TITLE, lang)}</b>\n\n{_t(TERMS_TEXT, lang)}",
            parse_mode="HTML",
            reply_markup=terms_kb.as_markup()
        )
        return  # ждём нажатия "Принимаю"

    # Условия уже приняты — стандартный онбординг
    await message.answer(
        text=_t(START_INSTRUCTION_TEXT, lang),
        parse_mode="HTML",
        reply_markup=get_main_menu(user_id)  # как у тебя и было без await
    )
    await message.answer(
        text=_t(START_VIDEO_INSTRUCTION_TEXT, lang),
        parse_mode="HTML",
    )
    await message.answer_photo(photo=FSInputFile("media/if.jpg"))


@router.callback_query(lambda c: c.data == "check_subs")
async def handle_check_subscription(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    # Эта кнопка по сути уже не нужна, но оставляем для совместимости
    user_id = callback.from_user.id
    logger.info(f"[SUB_CHECK] Проверка подписки для пользователя {user_id}")

    # Берём язык
    user = await get_user(user_id)
    lang = _get_lang(user)

    try:
        await callback.answer(_t(START_CHECKING, lang), show_alert=False)
    except Exception:
        pass

    # Повторяем ту же логику, что и в /start
    has_access = False
    if user_id == ADMIN_ID:
        has_access = True
    elif user:
        user_data = dict(user)
        is_paid = user_data.get("is_paid", False)
        payment_date = user_data.get("payment_date")
        if is_paid and payment_date:
            expire_date = payment_date + timedelta(days=SUBSCRIPTION_DAYS)
            if datetime.utcnow() < expire_date:
                has_access = True

    if has_access:
        full_name = callback.from_user.full_name or "-"
        await save_user(user_id, full_name)

        # --- ДОБАВЛЕНО: если соглашение ещё не принято — показываем вместо онбординга ---
        user_data = dict(user or {})
        if not user_data.get("terms_accepted", False):
            terms_kb = InlineKeyboardBuilder()
            terms_kb.row(
                types.InlineKeyboardButton(
                    text=_t(TERMS_ACCEPT_BTN, lang),
                    callback_data="accept_terms"
                )
            )
            await callback.message.answer(
                text=f"<b>{_t(TERMS_TITLE, lang)}</b>\n\n{_t(TERMS_TEXT, lang)}",
                parse_mode="HTML",
                reply_markup=terms_kb.as_markup()
            )
            return

        # Условия уже приняты — стандартный онбординг
        await callback.message.answer(
            text=_t(START_INSTRUCTION_TEXT, lang),
            parse_mode="HTML",
            reply_markup=get_main_menu(user_id)  # как у тебя и было без await
        )
        await callback.message.answer(
            text=_t(START_VIDEO_INSTRUCTION_TEXT, lang),
            parse_mode="HTML",
        )
        await callback.message.answer_photo(photo=FSInputFile("media/if.jpg"))
        return

    # Если доступа нет – предлагаем оплату
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        types.InlineKeyboardButton(
            text=_t(START_PAY_BUTTON, lang),
            url=TRIBUTE_PAYMENT_LINK,
        )
    )

    await callback.message.answer(
        _t(START_NO_ACCESS, lang),
        reply_markup=keyboard.as_markup(),
    )
    await callback.answer(_t(START_NO_ACCESS_ALERT, lang), show_alert=True)


# --- ДОБАВЛЕНО: обработчик кнопки "Принимаю" ---
@router.callback_query(F.data == "accept_terms")
async def handle_accept_terms(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user(user_id)
    lang = _get_lang(user)

    # Фиксируем принятие соглашения в БД (флаг + время)
    try:
        await set_terms_accepted(user_id)
    except Exception as e:
        logger.error(f"[TERMS] set_terms_accepted failed for {user_id}: {e}")

    # Убираем клавиатуру под соглашением (если возможно)
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    # Дальше — стандартные инструкции и меню (как было)
    await callback.message.answer(
        text=_t(START_INSTRUCTION_TEXT, lang),
        parse_mode="HTML",
        reply_markup=get_main_menu(user_id)  # как у тебя и было без await
    )

    await callback.message.answer(
        text=_t(START_VIDEO_INSTRUCTION_TEXT, lang),
        parse_mode="HTML",
    )

    await callback.message.answer_photo(photo=FSInputFile("media/if.jpg"))

    try:
        await callback.answer("✅ Принято", show_alert=False)
    except Exception:
        pass
