import random
import logging
from aiogram import Router, types
from handlers.texts.menu_texts import MAIN_MENU_TEXTS

router = Router()
logger = logging.getLogger(__name__)

CHANNEL_USERNAME = "@yourambitions"

# Список рабочих file_id мотивационных изображений
MOTIVATION_CONTENT = [
    # Посты канала (пересылка)
    ("post", 581),
    ("post", 579),
    ("post", 578),
    ("post", 576),
    ("post", 570),
]

@router.message(lambda msg: msg.text in [t["motivation"] for t in MAIN_MENU_TEXTS.values()])
async def show_motivation(message: types.Message):
    choice = random.choice(MOTIVATION_CONTENT)
    content_type, value = choice
    logger.info(f"[MOTIVATION] Выбран контент: {content_type} | {value}")

    if content_type == "photo":
        await message.answer_photo(value, caption="💪 Держи мотивацию!")
    else:  # post
        try:
            await message.bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_USERNAME,
                message_id=value
            )
        except Exception as e:
            logger.error(f"[MOTIVATION] Ошибка при пересылке поста {value}: {e}")
            await message.answer("❌ Ошибка при пересылке поста. Убедись, что бот админ в канале.")