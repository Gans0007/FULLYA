import logging
from datetime import datetime, timedelta, timezone
from random import choice

from aiogram import Router, Bot
from aiogram.types import ChatMemberUpdated
from aiogram.exceptions import TelegramBadRequest

from repositories.profiles.profile_repository import update_payment_status, get_user, ensure_paid_user
from repositories.referrals.referral_repo import get_referrer_id
from services.profile.xp_service import add_usdt  # ✅ импортируем начисление USDT
from handlers.texts.notifications_texts import PAID_REFERRAL_MESSAGES
import config

router = Router()
logger = logging.getLogger(__name__)

SUBSCRIPTION_DAYS = 30

@router.chat_member()
async def sync_subscription(event: ChatMemberUpdated, bot: Bot):
    user_id = event.new_chat_member.user.id
    chat_id = event.chat.id
    new_status = event.new_chat_member.status

    if chat_id == config.PUBLIC_CHANNEL_ID:
        now = datetime.now(timezone.utc)

        # Пользователь зашёл (новая оплата или автооплата)
                # Пользователь зашёл (новая оплата или автооплата)
        if new_status in {"member", "administrator", "creator"}:
            user = await get_user(user_id)
            if user:
                user_data = dict(user)
                payment_date = user_data.get("payment_date")
                is_paid = user_data.get("is_paid", False)

                if not is_paid or (payment_date and payment_date + timedelta(days=SUBSCRIPTION_DAYS) < now):
                    logger.info(f"[SYNC] {user_id} вошёл в канал — активируем подписку (новая оплата)")
                    await update_payment_status(user_id, True)

                    # 🔥 Начисляем 1 USDT рефереру, если есть
                    ref_row = await get_referrer_id(user_id)
                    if ref_row:
                        referrer_id = ref_row["referrer_id"]

                        await add_usdt(referrer_id, amount=1.0, reason="referral_paid")
                        logger.info(f"[REFERRAL USDT] Начислен 1 USDT пригласившему {referrer_id} за оплату {user_id}")

                        # Отправляем уведомление пригласившему
                        full_name = user_data.get("full_name", "Новый участник")
                        text = choice(PAID_REFERRAL_MESSAGES).format(name=full_name)

                        try:
                            await bot.send_message(referrer_id, text, parse_mode="HTML")
                            logger.info(f"[REFERRAL] Сообщение о платеже отправлено {referrer_id}")
                        except TelegramBadRequest as e:
                            logger.warning(f"[REFERRAL] Не удалось отправить сообщение {referrer_id}: {e}")
                else:
                    logger.info(f"[SYNC] {user_id} вошёл в канал — подписка уже активна, дату не обновляем")
            else:
                # ✅ Новый случай: оплатил Tribute и сразу вступил в канал, не заходя в бота
                full_name = (event.new_chat_member.user.full_name or "Новый участник").strip()
                try:
                    await ensure_paid_user(user_id=user_id, name=full_name)
                    logger.info(f"[SYNC] {user_id} вошёл в канал — не было в БД: created+paid ({full_name})")
                except Exception as e:
                    logger.exception(f"[SYNC] ensure_paid_user failed user_id={user_id}: {e}")
                    await update_payment_status(user_id, True)

                # 🔥 Начисляем 1 USDT рефереру, если есть
                try:
                    ref_row = await get_referrer_id(user_id)
                    if ref_row:
                        referrer_id = ref_row["referrer_id"]
                        await add_usdt(referrer_id, amount=1.0, reason="referral_paid")
                        logger.info(f"[REFERRAL USDT] +1 USDT рефереру {referrer_id} за оплату {user_id}")

                        text = choice(PAID_REFERRAL_MESSAGES).format(name=full_name)
                        try:
                            await bot.send_message(referrer_id, text, parse_mode="HTML")
                            logger.info(f"[REFERRAL] Сообщение о платеже отправлено {referrer_id}")
                        except TelegramBadRequest as e:
                            logger.warning(f"[REFERRAL] Не удалось отправить сообщение {referrer_id}: {e}")
                except Exception as e:
                    logger.warning(f"[REFERRAL] Не удалось обработать рефералку для {user_id}: {e}")


        elif new_status == "kicked":
            logger.info(f"[SYNC] {user_id} кикнут трибутом — подписка закончилась")
            await update_payment_status(user_id, False)

            try:
                await bot.ban_chat_member(config.PUBLIC_CHAT_ID, user_id)
                await bot.unban_chat_member(config.PUBLIC_CHAT_ID, user_id)
                logger.info(f"[SYNC] {user_id} удалён из чата 2")
            except Exception as e:
                logger.error(f"[SYNC] Ошибка при удалении {user_id} из чата 2: {e}")

        elif new_status == "left":
            user = await get_user(user_id)
            if user:
                user_data = dict(user)
                payment_date = user_data.get("payment_date")
                if payment_date:
#последн обновл
                    pd = payment_date
                    if pd.tzinfo is None:
                        # если дата без таймзоны, помечаем как UTC
                        pd = pd.replace(tzinfo=timezone.utc)
                    else:
                        # нормализуем в UTC (если вдруг с другим tz)
                        pd = pd.astimezone(timezone.utc)

                    expire_date = pd + timedelta(days=SUBSCRIPTION_DAYS)
                    if now >= expire_date:

                        logger.info(f"[SYNC] {user_id} вышел и срок подписки истёк ({expire_date}) — отключаем")
                        await update_payment_status(user_id, False)
                        try:
                            await bot.ban_chat_member(config.PUBLIC_CHAT_ID, user_id)
                            await bot.unban_chat_member(config.PUBLIC_CHAT_ID, user_id)
                            logger.info(f"[SYNC] {user_id} удалён из чата 2")
                        except Exception as e:
                            logger.error(f"[SYNC] Ошибка при удалении {user_id} из чата 2: {e}")
                    else:
                        logger.info(f"[SYNC] {user_id} вышел, но срок подписки ещё действует до {expire_date}. Доступ сохраняется.")
                else:
                    logger.info(f"[SYNC] {user_id} вышел, но в базе нет payment_date — ничего не делаем")
