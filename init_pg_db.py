import os
from dotenv import load_dotenv
from databases import Database
import asyncio

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

async def init_postgres_db():
    async with database:
        await database.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            name TEXT,
            xp_balance INTEGER DEFAULT 0,
            usdt_balance REAL DEFAULT 0,
            withdrawn REAL DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            created_habits INTEGER DEFAULT 0,
            special_reward BOOLEAN DEFAULT FALSE,
            finished_habits INTEGER DEFAULT 0,
            finished_challenges INTEGER DEFAULT 0,
            active_days INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            last_confirmation_date DATE,
            active_referrals INTEGER DEFAULT 0,
            notification_tone TEXT DEFAULT 'mixed',
            language VARCHAR(5) DEFAULT 'ru',
            goals_reminder_at TIMESTAMPTZ,
            dreams_reminder_at TIMESTAMPTZ
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            referrer_id BIGINT,
            invited_id BIGINT PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            is_active BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (referrer_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (invited_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            days INTEGER NOT NULL,
            description TEXT,
            done_days INTEGER DEFAULT 0,
            is_challenge BOOLEAN DEFAULT FALSE,
            confirm_type TEXT DEFAULT 'media',
            created_at TIMESTAMPTZ DEFAULT NOW(),
            is_active BOOLEAN DEFAULT TRUE,    
            challenge_id TEXT, 
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS pending_videos (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            video_link TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved BOOLEAN DEFAULT FALSE,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS reward_history (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('xp', 'usdt')),
            reason TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS confirmations (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            habit_id INTEGER NOT NULL,
            datetime TIMESTAMP,
            file_id TEXT,
            file_type TEXT,
            confirmed BOOLEAN,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS timezones (
            user_id BIGINT PRIMARY KEY,
            offset_minutes INTEGER
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS reset_flags (
            user_id BIGINT,
            date DATE,
            PRIMARY KEY (user_id, date),
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        await database.execute("""
        CREATE TABLE IF NOT EXISTS completed_challenges (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            challenge_id TEXT NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)



        await database.execute("""
        CREATE TABLE IF NOT EXISTS completed_habits (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            days INTEGER,
            done_days INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)


        # Таблица целей
        await database.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            text TEXT NOT NULL,
            is_done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            done_at TIMESTAMP,
            last_reminder TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        # Таблица планов
        await database.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            goal_id INTEGER,
            text TEXT NOT NULL,
            is_done BOOLEAN DEFAULT FALSE,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(goal_id) REFERENCES goals(id) ON DELETE CASCADE
        );
        """)

        # Таблица мечт
        await database.execute("""
        CREATE TABLE IF NOT EXISTS dreams (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            text TEXT NOT NULL,
            is_done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            done_at TIMESTAMP,
            last_reminder TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        # Таблица для фотографий, привязанных к мечтам
        await database.execute("""
        CREATE TABLE IF NOT EXISTS dream_photos (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            dream_id INTEGER NOT NULL,
            photo_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(dream_id) REFERENCES dreams(id) ON DELETE CASCADE
        );
        """)


        await database.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, code),
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)


        print("✅ PostgreSQL таблицы инициализированы.")


if __name__ == "__main__":
    asyncio.run(init_postgres_db())
