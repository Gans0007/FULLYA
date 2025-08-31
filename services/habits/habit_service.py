from db.db import database
# get_current_time больше не нужен здесь

async def save_habit(
    user_id: int,
    name: str,
    days: int,
    description: str,
    is_challenge: bool = False,
    confirm_type: str = 'media',
    challenge_id: str | None = None
):
    await database.execute("""
        INSERT INTO habits (
            user_id, name, days, description,
            done_days, is_challenge, confirm_type, created_at, challenge_id
        )
        VALUES (
            :user_id, :name, :days, :description,
            0, :is_challenge, :confirm_type, NOW(), :challenge_id
        )
    """, {
        "user_id": user_id,
        "name": name,
        "days": days,
        "description": description,
        "is_challenge": is_challenge,
        "confirm_type": confirm_type,
        "challenge_id": challenge_id
    })
