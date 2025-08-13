import logging
from db.db import database
from handlers.texts.achievements_texts import ACHIEVEMENTS_TEXTS, HEADERS  # ✅ мультиязычные тексты и заголовки

logger = logging.getLogger(__name__)

# ----------------- helpers -----------------

async def _get_user_lang(user_id: int) -> str:
    """
    Берём язык пользователя из users.language.
    Нормализуем и делаем умные фолбэки (ua->uk, ru-RU->ru и т.п.).
    Порядок фолбэков: user -> ru -> uk -> en -> первый доступный.
    """
    lang = await database.fetch_val(
        "SELECT language FROM users WHERE user_id = :uid",
        {"uid": user_id}
    )
    lang = (lang or "").strip().lower()

    # Нормализация
    if lang.startswith("ua"):
        lang = "uk"
    if lang.startswith(("ru", "uk", "en")):
        lang = lang[:2]

    if lang in ACHIEVEMENTS_TEXTS:
        return lang

    for candidate in ("ru", "uk", "en"):
        if candidate in ACHIEVEMENTS_TEXTS:
            return candidate

    # Совсем крайний случай
    return next(iter(ACHIEVEMENTS_TEXTS.keys()))


def _get_text_for(code: str, lang: str) -> str | None:
    """
    Возвращает текст достижения по коду с каскадным фолбэком:
    lang -> ru -> uk -> en.
    """
    for k in (lang, "ru", "uk", "en"):
        d = ACHIEVEMENTS_TEXTS.get(k, {})
        if code in d:
            return d[code]
    return None


def _code_exists_anywhere(code: str) -> bool:
    """Есть ли такой код хотя бы в одном языке."""
    return any(code in d for d in ACHIEVEMENTS_TEXTS.values())


# ----------------- public API -----------------

async def grant_achievement(user_id: int, code: str, bot=None):
    """
    Выдает достижение пользователю, если оно ещё не было выдано.
    Отправляет локализованное сообщение и начисляет XP.
    """
    logger.info(f"[ACHIEVEMENT] Попытка выдать достижение {code} пользователю {user_id}")

    if not _code_exists_anywhere(code):
        logger.warning(f"[ACHIEVEMENT] Код {code} не найден в ACHIEVEMENTS_TEXTS ни в одном языке")
        return False

    new_id = await database.fetch_val(
        """
        INSERT INTO achievements (user_id, code)
        VALUES (:user_id, :code)
        ON CONFLICT DO NOTHING
        RETURNING id
        """,
        {"user_id": user_id, "code": code}
    )

    # Если запись уже существует (конфликт), то ничего не делаем
    if not new_id:
        logger.info(f"[ACHIEVEMENT] Достижение {code} уже было у пользователя {user_id}")
        return False

    logger.info(f"[ACHIEVEMENT] Новое достижение {code} добавлено пользователю {user_id}")

    # Новое достижение: отправляем сообщение
    if bot:
        lang = await _get_user_lang(user_id)
        header = HEADERS.get(lang) or HEADERS.get("ru") or "🏆 Achievement:"
        text = _get_text_for(code, lang) or code  # на всякий
        try:
            await bot.send_message(
                user_id,
                f"{header}\n<b>{text}</b>",
                parse_mode="HTML"
            )
            logger.info(f"[ACHIEVEMENT] Сообщение о достижении {code} отправлено пользователю {user_id}")
        except Exception as e:
            logger.warning(f"[ACHIEVEMENT] Не удалось отправить сообщение пользователю {user_id}: {e}")

        # Автоматическое начисление XP за достижение
        try:
            from services.profile.xp_service import xp_for_achievement
            await xp_for_achievement(user_id, bot)
            logger.info(f"[ACHIEVEMENT] Начислено XP за достижение {code} пользователю {user_id}")
        except Exception as e:
            logger.warning(f"[ACHIEVEMENT] Не удалось начислить XP за достижение {code}: {e}")

    return True


async def check_and_grant(user_id: int, event_type: str, value: int, bot=None):
    """
    Универсальная проверка достижений.
    Возвращает True, если достижение было выдано впервые,
    и False, если достижение уже было.
    """
    logger.info(f"[ACHIEVEMENT] Проверка достижений: user_id={user_id}, event_type={event_type}, value={value}")

    thresholds = {
        "streak": [3, 7, 14, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
        "habit_create": [1, 5, 10],
        "habit_complete": [1, 5, 10, 25],
        "habit_done": [10, 30, 50, 70, 90, 110],
        "challenge_create": [1, 5, 10],
        "challenge_done": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        "active_days": [1, 10, 25, 40, 60, 80, 110, 140, 170, 200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500, 530, 560, 590, 620, 650, 680, 710, 740, 770, 800, 830, 860, 890, 920, 950, 980, 1000],
        "invite": [1, 3, 5, 10, 25],
        "league": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    }

    if event_type not in thresholds:
        logger.warning(f"[ACHIEVEMENT] Неизвестный тип события: {event_type}")
        return False

    for t in thresholds[event_type]:
        if value == t:  # ровно достигли порога
            code = f"{event_type}_{t}"
            logger.info(f"[ACHIEVEMENT] Порог достигнут: {code} для user_id={user_id}")

            # Выдаём достижение локально (без самовызова из handlers.achievements)
            result = await grant_achievement(user_id, code, bot)

            if result:
                logger.info(f"[ACHIEVEMENT] Новое достижение выдано: {code} для user_id={user_id}")
            else:
                logger.info(f"[ACHIEVEMENT] Достижение {code} уже есть у user_id={user_id}")

            return result

    logger.debug(f"[ACHIEVEMENT] Нет порогов для выдачи достижения по event_type={event_type} и value={value}")
    return False
