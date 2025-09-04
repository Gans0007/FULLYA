from db.db import database
from utils.timezones import get_current_time

async def save_user(user_id: int, name: str | None = None):
    await database.execute("""
        INSERT INTO users (user_id, name, created_at)
        VALUES (:user_id, :name, NOW())
        ON CONFLICT (user_id) DO NOTHING
    """, {
        "user_id": user_id,
        "name": name or "—",})



async def get_user(user_id: int):
    return await database.fetch_one("""
        SELECT * FROM users WHERE user_id = :user_id
    """, {"user_id": user_id})


#Обо мне - профиль
async def get_profile(user_id: int) -> dict | None:
    """Получаем профиль пользователя"""
    row = await database.fetch_one("""
        SELECT * FROM profiles WHERE user_id = :uid
    """, {"uid": user_id})
    return dict(row) if row else None


async def save_profile(user_id: int, name: str, username: str, age: int,
                       specialization: str, help_text: str, message: str):
    """Создаём или обновляем профиль"""
    query = """
    INSERT INTO profiles (user_id, name, username, age, specialization, help_text, message)
    VALUES (:user_id, :name, :username, :age, :specialization, :help_text, :message)
    ON CONFLICT(user_id) DO UPDATE SET
        name=excluded.name,
        username=excluded.username,
        age=excluded.age,
        specialization=excluded.specialization,
        help_text=excluded.help_text,
        message=excluded.message
    """
    await database.execute(query, {
        "user_id": user_id,
        "name": name,
        "username": username,
        "age": age,
        "specialization": specialization,
        "help_text": help_text,
        "message": message
    })


async def update_profile_field(user_id: int, field: str, value, username: str):
    """Обновляем одно поле в профиле"""
    # Защита от SQL-инъекций — проверяем допустимые поля
    allowed_fields = {"name", "age", "specialization", "help", "message", "is_visible"}
    if field not in allowed_fields:
        raise ValueError(f"Недопустимое поле: {field}")

    db_field = "help_text" if field == "help" else field

    query = f"""
        UPDATE profiles
        SET {db_field} = :value, username = :username
        WHERE user_id = :uid
    """
    await database.execute(query, {
        "value": value,
        "username": username,
        "uid": user_id
    })

#оплата
async def update_payment_status(user_id: int, is_paid: bool):
    query = """
    UPDATE users
    SET is_paid = :is_paid,
        payment_date = CASE WHEN :is_paid THEN NOW() ELSE payment_date END
    WHERE user_id = :user_id
    """
    await database.execute(query, {"user_id": user_id, "is_paid": is_paid})



async def set_terms_accepted(user_id: int):
    query = """
        UPDATE users
        SET terms_accepted = TRUE,
            terms_accepted_at = NOW()
        WHERE user_id = :user_id
    """
    await database.execute(query=query, values={"user_id": user_id})


# --- NEW: идемпотентная фиксация оплаты и создание пользователя при необходимости ---
async def ensure_paid_user(user_id: int, name: str | None = None) -> None:
    """
    Создаёт пользователя (если его ещё нет) и активирует подписку:
      - is_paid = TRUE
      - payment_date = NOW()
    Если пользователь уже есть — обновляет is_paid и payment_date.
    """
    query = """
    INSERT INTO users (user_id, name, is_paid, payment_date, created_at)
    VALUES (:user_id, :name, TRUE, NOW(), NOW())
    ON CONFLICT (user_id) DO UPDATE
    SET is_paid = TRUE,
        payment_date = NOW(),
        name = COALESCE(users.name, EXCLUDED.name)
    """
    await database.execute(query, {"user_id": user_id, "name": name or "—"})

