import asyncio
from aiogram.types import Message, CallbackQuery

async def safe_replace_message(message: Message, text: str, reply_markup=None, delay: float = 0.4, parse_mode: str = None):
    try:
        await message.delete()
        await asyncio.sleep(delay)
    except Exception:
        pass
    await message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)

async def try_edit_message(callback_or_message, text: str, markup=None, parse_mode: str = None):
    try:
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.edit_text(text, reply_markup=markup, parse_mode=parse_mode)
        elif isinstance(callback_or_message, Message):
            await callback_or_message.edit_text(text, reply_markup=markup, parse_mode=parse_mode)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"[UI] Ошибка при редактировании сообщения: {e}")
