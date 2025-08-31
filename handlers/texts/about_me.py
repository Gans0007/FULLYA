
ABOUT_MENU_TEXTS = {
    "ru": {
        "referrals": "🤝 Реферальная система",
        "stats": "📊 Статистика",
        "profile": "👤 Профиль",
        "participants": "👥 Участники",
        "settings": "⚙️ Настройки",
    },
    "uk": {
        "referrals": "🤝 Реферальна система",
        "stats": "📊 Статистика",
        "profile": "👤 Профіль",
        "participants": "👥 Учасники",
        "settings": "⚙️ Налаштування",
    },
    "en": {
        "referrals": "🤝 Referral System",
        "stats": "📊 Stats",
        "profile": "👤 Profile",
        "participants": "👥 Members",
        "settings": "⚙️ Settings",
    }
}


#---------- РЕФЕРАЛКА----------



REFERRAL_TEXTS = {
    "ru": {
        "program_title": "<b>👥 Твоя реферальная программа</b>\n\n",
        "link": "🔗 <b>Ссылка:</b> {referral_link}\n\n",
        "total_invited": "📊 Всего приглашено: <b>{total}</b>\n",
        "active_paid": "🔥 Активных (оплатили): <b>{active}</b>\n",
        "balance": "💰 На балансе: <b>{usdt:.2f} USDT</b>\n",
        "withdrawn": "🪙 Выведено: <b>{withdrawn:.2f} USDT</b>",
        "active_friends_title": "<b>✅ Активные друзья:</b>",
        "active_friend_item": "• {name}",
        "active_friend_item_with_username": "• {name} (@{username})",
        "unknown_friend": "• Пользователь {id}",

        # Кнопки
        "btn_withdraw": "💸 Вывод",
        "btn_rules": "📜 Правила",
        "btn_back": "⬅️ Назад",

        # Правила
        "rules_title": "<b>📜 Правила реферальной программы</b>\n\n",
        "rules_who_title": "<b>Кто может участвовать</b>\n",
        "rules_who_text": (
            "В реферальной программе может участвовать любой пользователь, даже если его подписка закончилась. "
            "Реферальная ссылка остаётся активной навсегда.\n\n"
        ),
        "rules_active_title": "<b>Что такое активный реферал</b>\n",
        "rules_active_text": "Активным считается реферал, который оплатил подписку.\n\n",
        "rules_reward_title": "<b>Вознаграждение</b>\n",
        "rules_reward_text": (
            "• За каждого активного реферала вы получаете 10% от стоимости его подписки "
            "(пример: при подписке за 10 USDT — 1 USDT на ваш баланс).\n"
            "• Если реферал продлевает подписку, вы будете получать бонус каждый месяц.\n\n"
        ),
        "rules_accrual_title": "<b>Начисление бонусов</b>\n",
        "rules_accrual_text": (
            "Начисление происходит моментально, как только реферал оплатил и вошёл в канал.\n\n"
        ),
        "rules_withdraw_title": "<b>Вывод средств</b>\n",
        "rules_withdraw_text": (
            "• Минимальная сумма вывода — 1 USDT.\n"
            "• Вывод осуществляется на баланс биржи.\n"
            "• Если вы не знаете, как создать биржевой аккаунт, наш менеджер поможет вам с этим."
        ),
    },

    "en": {
        "program_title": "<b>👥 Your Referral Program</b>\n\n",
        "link": "🔗 <b>Link:</b> {referral_link}\n\n",
        "total_invited": "📊 Total invited: <b>{total}</b>\n",
        "active_paid": "🔥 Active (paid): <b>{active}</b>\n",
        "balance": "💰 Balance: <b>{usdt:.2f} USDT</b>\n",
        "withdrawn": "🪙 Withdrawn: <b>{withdrawn:.2f} USDT</b>",
        "active_friends_title": "<b>✅ Active Friends:</b>",
        "active_friend_item": "• {name}",
        "active_friend_item_with_username": "• {name} (@{username})",
        "unknown_friend": "• User {id}",

        # Buttons
        "btn_withdraw": "💸 Withdraw",
        "btn_rules": "📜 Rules",
        "btn_back": "⬅️ Back",

        # Rules
        "rules_title": "<b>📜 Referral Program Rules</b>\n\n",
        "rules_who_title": "<b>Who Can Participate</b>\n",
        "rules_who_text": (
            "Any user can participate in the referral program, even if their subscription has expired. "
            "The referral link remains active forever.\n\n"
        ),
        "rules_active_title": "<b>What Is an Active Referral</b>\n",
        "rules_active_text": "An active referral is a user who has paid for a subscription.\n\n",
        "rules_reward_title": "<b>Reward</b>\n",
        "rules_reward_text": (
            "• For each active referral, you receive 10% of their subscription cost "
            "(example: if the subscription is 10 USDT — you get 1 USDT to your balance).\n"
            "• If the referral renews their subscription, you will receive a bonus every month.\n\n"
        ),
        "rules_accrual_title": "<b>Bonus Accrual</b>\n",
        "rules_accrual_text": (
            "Bonuses are credited instantly once the referral has paid and joined the channel.\n\n"
        ),
        "rules_withdraw_title": "<b>Withdrawal</b>\n",
        "rules_withdraw_text": (
            "• Minimum withdrawal amount — 1 USDT.\n"
            "• Withdrawal is made to the exchange balance.\n"
            "• If you don’t know how to create an exchange account, our manager will help you."
        ),
    },

    "uk": {
        "program_title": "<b>👥 Твоя реферальна програма</b>\n\n",
        "link": "🔗 <b>Посилання:</b> {referral_link}\n\n",
        "total_invited": "📊 Всього запрошено: <b>{total}</b>\n",
        "active_paid": "🔥 Активних (сплатили): <b>{active}</b>\n",
        "balance": "💰 На балансі: <b>{usdt:.2f} USDT</b>\n",
        "withdrawn": "🪙 Виведено: <b>{withdrawn:.2f} USDT</b>",
        "active_friends_title": "<b>✅ Активні друзі:</b>",
        "active_friend_item": "• {name}",
        "active_friend_item_with_username": "• {name} (@{username})",
        "unknown_friend": "• Користувач {id}",

        # Кнопки
        "btn_withdraw": "💸 Вивід",
        "btn_rules": "📜 Правила",
        "btn_back": "⬅️ Назад",

        # Правила
        "rules_title": "<b>📜 Правила реферальної програми</b>\n\n",
        "rules_who_title": "<b>Хто може брати участь</b>\n",
        "rules_who_text": (
            "У реферальній програмі може брати участь будь-який користувач, навіть якщо його підписка закінчилася. "
            "Реферальне посилання залишається активним назавжди.\n\n"
        ),
        "rules_active_title": "<b>Що таке активний реферал</b>\n",
        "rules_active_text": "Активним вважається реферал, який сплатив підписку.\n\n",
        "rules_reward_title": "<b>Винагорода</b>\n",
        "rules_reward_text": (
            "• За кожного активного реферала ви отримуєте 10% від вартості його підписки "
            "(приклад: при підписці за 10 USDT — 1 USDT на ваш баланс).\n"
            "• Якщо реферал продовжує підписку, ви будете отримувати бонус кожного місяця.\n\n"
        ),
        "rules_accrual_title": "<b>Нарахування бонусів</b>\n",
        "rules_accrual_text": (
            "Нарахування відбувається миттєво, як тільки реферал сплатив і приєднався до каналу.\n\n"
        ),
        "rules_withdraw_title": "<b>Вивід коштів</b>\n",
        "rules_withdraw_text": (
            "• Мінімальна сума виводу — 1 USDT.\n"
            "• Вивід здійснюється на баланс біржі.\n"
            "• Якщо ви не знаєте, як створити біржовий акаунт, наш менеджер допоможе вам з цим."
        ),
    }
}




#---------- СТАТИСТИКА----------


# handlers/texts/about_me/statistics_texts.py

STATISTICS_TEXTS = {
    "ru": {
        "stats_title": "<b>📊 Ваша статистика</b>",
        "league": "🏅 <b>Лига:</b> {emoji} {league}      [XP: {xp} / {xp_to_next}]",
        "current_streak": "🔥 <b>Текущий стрик:</b> {days} дней подряд",
        "best_streak": "🏆 <b>Лучший стрик:</b> {days} дней подряд",
        "active_days": "🎯 <b>Активных дней:</b> {days} дней",
        "finished_habits": "✅ <b>Привычек завершено:</b> {count}",
        "finished_challenges": "🏁 <b>Челленджей завершено:</b> {count}",
        "achievements": "🎖 <b>Достижения:</b> ({have}/{total})",
        "reward": "🎁 <b>Подарок от Your Ambitions:</b> {value}",
        "created_at": "📅 <b>Дата регистрации:</b> {date}",
        "back": "🔙 Назад",
        "no_username": "Без ника",
    },
    "uk": {
        "stats_title": "<b>📊 Ваша статистика</b>",
        "league": "🏅 <b>Ліга:</b> {emoji} {league}      [XP: {xp} / {xp_to_next}]",
        "current_streak": "🔥 <b>Поточна серія:</b> {days} днів поспіль",
        "best_streak": "🏆 <b>Найкраща серія:</b> {days} днів поспіль",
        "active_days": "🎯 <b>Активних днів:</b> {days} днів",
        "finished_habits": "✅ <b>Звичок завершено:</b> {count}",
        "finished_challenges": "🏁 <b>Челенджів завершено:</b> {count}",
        "achievements": "🎖 <b>Досягнення:</b> ({have}/{total})",
        "reward": "🎁 <b>Подарунок від Your Ambitions:</b> {value}",
        "created_at": "📅 <b>Дата реєстрації:</b> {date}",
        "back": "🔙 Назад",
        "no_username": "Без ніку",
    },
    "en": {
        "stats_title": "<b>📊 Your statistics</b>",
        "league": "🏅 <b>League:</b> {emoji} {league}      [XP: {xp} / {xp_to_next}]",
        "current_streak": "🔥 <b>Current streak:</b> {days} days in a row",
        "best_streak": "🏆 <b>Best streak:</b> {days} days in a row",
        "active_days": "🎯 <b>Active days:</b> {days} days",
        "finished_habits": "✅ <b>Habits completed:</b> {count}",
        "finished_challenges": "🏁 <b>Challenges completed:</b> {count}",
        "achievements": "🎖 <b>Achievements:</b> ({have}/{total})",
        "reward": "🎁 <b>Gift from Your Ambitions:</b> {value}",
        "created_at": "📅 <b>Registration date:</b> {date}",
        "back": "🔙 Back",
        "no_username": "No username",
    },
}





#----------ПРОФИЛЬ----------


PROFILE_TEXTS = {
    "ru": {
        # Верхняя плашка про видимость
        "visibility_open": "👁 <b>Каждый может посмотреть, чем ты можешь быть полезен</b>",
        "visibility_closed": "🙈 <b>Свой профиль видишь только ты</b>",

        # Подписи полей
        "label_name": "👤 Имя",
        "label_username": "🆔 Ник",
        "label_age": "🎂 Возраст",
        "label_spec": "💼 Профессия",
        "label_help": "📝 Хобби/Польза другим",
        "label_message": "🤝 Соц.Сеть",

        # Пустой профиль
        "profile_empty": "🗺 Профиль пока не заполнен. Нажми ✏️ чтобы начать.",

        # Кнопки
        "btn_open": "🔓 Открытый",
        "btn_closed": "🔒 Скрытый",
        "btn_edit": "✏️ Редактировать",
        "btn_back": "🔙 Назад",

        # Экран 'Обо мне'
        "about_header": "USDT: {usdt:.2f} | XP: {xp} | Лига: {liga}\n\n«{quote}»",
    },

    "uk": {
        "visibility_open": "👁 <b>Кожен може побачити, чим ти можеш бути корисним</b>",
        "visibility_closed": "🙈 <b>Свій профіль бачиш лише ти</b>",

        "label_name": "👤 Ім'я",
        "label_username": "🆔 Нік",
        "label_age": "🎂 Вік",
        "label_spec": "💼 Професія",
        "label_help": "💡 Хоббі/Користь іншим",
        "label_message": "🤝 Соц.Мережа",

        "profile_empty": "🗺 Профіль ще не заповнений. Натисни ✏️, щоб почати.",

        "btn_open": "🔓 Відкритий",
        "btn_closed": "🔒 Прихований",
        "btn_edit": "✏️ Редагувати",
        "btn_back": "🔙 Назад",

        "about_header": "USDT: {usdt:.2f} | XP: {xp} | Ліга: {liga}\n\n«{quote}»",
    },

    "en": {
        "visibility_open": "👁 <b>Everyone can see how you can help</b>",
        "visibility_closed": "🙈 <b>Only you can see your profile</b>",

        "label_name": "👤 Name",
        "label_username": "🆔 Username",
        "label_age": "🎂 Age",
        "label_spec": "💼 Profession",
        "label_help": "📝 Hobby/Useful for",
        "label_message": "🤝 Social",

        "profile_empty": "🗺 The profile is empty yet. Tap ✏️ to start.",

        "btn_open": "🔓 Public",
        "btn_closed": "🔒 Private",
        "btn_edit": "✏️ Edit",
        "btn_back": "🔙 Back",

        "about_header": "USDT: {usdt:.2f} | XP: {xp} | League: {liga}\n\n“{quote}”",
    },
}


PROFILE_FSM_TEXTS = {
    "ru": {
        "start_name": "👤 Введи своё имя:",
        "select_field": "🔧 Что хочешь изменить?",
        "fields": {
            "name": "🖊 Имя",
            "age": "🎂 Возраст",
            "specialization": "💼 Профессия",
            "help": "📝 Чем полезен",
            "message": "🤝 Соц.Сеть",
        },
        "prompts": {
            "name": "👤 Введи новое имя:",
            "age": "🎂 Введи новый возраст:",
            "specialization": "💼 Укажи новую профессию (не больше 15 символов):",
            "help": "📝 Твои хобби, или чем ты можешь быть полезен другим? (не больше 100 символов)",
            "message": "🤝 Добавь свою социальную сеть (не больше 200 символов):",
        },
        "cancel": "❌ Отмена",
        "cancelled": "❌ Отменено. Возвращаю в профиль.",
        "errors": {
            "age": "❌ Возраст должен быть числом. Попробуй снова.",
            "specialization": "❌ Специализация должна быть не длиннее 15 символов.",
            "help": "❌ Описание хобби/пользы не должно превышать 100 символов.",
            "message": "❌ Соц.сеть не должны быть длиннее 200 символов.",
        },
        "view_changes": "👀 Просмотреть изменения",
        "updated": "✅ Обновлено, просмотреть можно нажав на кнопку ниже!",
        "step_age": "🎂 Введи возраст:",
        "step_spec": "💼 Напиши свою профессию (не больше 15 символов):",
        "step_help": "📝 Твои хобби или чем ты можешь быть полезен другим? (не больше 100 символов):",
        "step_message": "🤝 Добавь свою социальную сеть (не больше 200 символов):",
        "created": "✅ Профиль успешно создан!"
    },
    "uk": {
        "start_name": "👤 Введи своє ім'я:",
        "select_field": "🔧 Що хочеш змінити?",
        "fields": {
            "name": "🖊 Ім'я",
            "age": "🎂 Вік",
            "specialization": "🧠 Професія",
            "help": "💡 Корисний",
            "message": "🤝 Соц.Мережа",
        },
        "prompts": {
            "name": "👤 Введи нове ім'я:",
            "age": "🎂 Введи новий вік:",
            "specialization": "💼 Вкажи нову професію (не більше 15 символів):",
            "help": "📝 Твої хоббі або чим ти можеш бути корисний іншим? (не більше 100 символів)",
            "message": "🤝 Додай свою соціальну мережу (не більше 200 символів):",
        },
        "cancel": "❌ Скасувати",
        "cancelled": "❌ Скасовано. Повертаю до профілю.",
        "errors": {
            "age": "❌ Вік має бути числом. Спробуй ще раз.",
            "specialization": "❌ Професія має бути не довше 15 символів.",
            "help": "❌ Опис користі не має перевищувати 100 символів.",
            "message": "❌ Соц.мережа не мають бути довші за 200 символів.",
        },
        "view_changes": "👀 Переглянути зміни",
        "updated": "✅ Оновлено, переглянути можна натиснувши на кнопку нижче!",
        "step_age": "🎂 Введи вік:",
        "step_spec": "💼 Напиши свою Професію (не більше 15 символів):",
        "step_help": "📝 Твої хоббі або чим ти можеш бути корисний іншим? (не більше 100 символів):",
        "step_message": "🤝 Додай свою соціальну мережу (не більше 200 символів):",
        "created": "✅ Профіль успішно створено!"
    },
    "en": {
        "start_name": "👤 Enter your name:",
        "select_field": "🔧 What do you want to change?",
        "fields": {
            "name": "🖊 Name",
            "age": "🎂 Age",
            "specialization": "💼 My Profession",
            "help": "📝 Useful for",
            "message": "🤝 Social",
        },
        "prompts": {
            "name": "👤 Enter new name:",
            "age": "🎂 Enter new age:",
            "specialization": "💼 Enter new profession (max 15 chars):",
            "help": "📝 Your hobby or how can you be useful to others? (max 100 chars)",
            "message": "🤝 Add your social network (max 200 chars):",
        },
        "cancel": "❌ Cancel",
        "cancelled": "❌ Cancelled. Returning to profile.",
        "errors": {
            "age": "❌ Age must be a number. Try again.",
            "specialization": "❌ Profession must be 15 chars or less.",
            "help": "❌ Help description must be 70 chars or less.",
            "message": "❌ Social must be 200 chars or less.",
        },
        "view_changes": "👀 View changes",
        "updated": "✅ Updated, you can view it by pressing the button below!",
        "step_age": "🎂 Enter age:",
        "step_spec": "💼 Enter your profession (max 15 chars):",
        "step_help": "📝 Your hobby or how can you be useful to others? (max 100 chars):",
        "step_message": "🤝 Add your social network (max 200 chars):",
        "created": "✅ Profile successfully created!"
    }
}





#----------УЧАСТНИКИ----------



MEMBERS_TEXTS = {
    "ru": {
        "age": "🎂 Возраст: {age}",
        "spec": "💼 Профессия: {spec}",
        "help": "📝 Хобби: {help}",
        "age_not_set": "Не указан",
        "spec_not_set": "Не указана",
        "help_not_set": "Нет описания",
        "participants_title": "👥 Участники, заполнившие профиль:",
        "back_to_menu": "В меню выбора",
        "nav_back": "⬅️ Назад",
        "nav_forward": "Вперёд ➡️",
        "profile_not_found": "Профиль не найден.",
        "card_back": "🔙 Назад",
        # добавлено
        "social": "🌐 Соцсеть: {social}",
        "social_not_set": "Не указана",
        "btn_contact": "✉️ Написать"
    },
    "uk": {
        "age": "🎂 Вік: {age}",
        "spec": "💼 Профессія: {spec}",
        "help": "📝 Хоббі: {help}",
        "age_not_set": "Не вказано",
        "spec_not_set": "Не вказана",
        "help_not_set": "Немає опису",
        "participants_title": "👥 Учасники, які заповнили профіль:",
        "back_to_menu": "У меню вибору",
        "nav_back": "⬅️ Назад",
        "nav_forward": "Вперед ➡️",
        "profile_not_found": "Профіль не знайдено.",
        "card_back": "🔙 Назад",
        # добавлено
        "social": "🌐 Соцмережа: {social}",
        "social_not_set": "Не вказана",
        "btn_contact": "✉️ Написати"
    },
    "en": {
        "age": "🎂 Age: {age}",
        "spec": "💼 Profession: {spec}",
        "help": "📝 Hobby: {help}",
        "age_not_set": "Not set",
        "spec_not_set": "Not set",
        "help_not_set": "No description",
        "participants_title": "👥 Participants who filled out the profile:",
        "back_to_menu": "Back to menu",
        "nav_back": "⬅️ Back",
        "nav_forward": "Forward ➡️",
        "profile_not_found": "Profile not found.",
        "card_back": "🔙 Back",
        # добавлено
        "social": "🌐 Social: {social}",
        "social_not_set": "Not set",
        "btn_contact": "✉️ Contact"
    }
}




#----------НАСТРОЙКИ----------

# ---------- НАСТРОЙКИ (мультиязычность тонов уведомлений + кнопки/сообщения) ----------

# Код тона -> локализованные метки
NOTIFICATION_TONES = {
    "soft": {"ru": "🧘 Мягкие", "uk": "🧘 М’які", "en": "🧘 Soft"},
    "hard": {"ru": "🥊 Жёсткие", "uk": "🥊 Жорсткі", "en": "🥊 Hard"},
    "mixed": {"ru": "😈 Очень", "uk": "😈 Дуже", "en": "😈 Very"},
}

ABOUT_OPTIONS_TEXTS = {
    "ru": {
        "title": "⚙️ Настройки",
        "description": "Выбери стиль уведомлений и язык интерфейса.",
        "notification_label": "🔔 Стиль уведомлений",
        "language_label": "🌐 Язык",

        # Кнопки тонов
        "btn_tone_soft": "🧘 Мягкие",
        "btn_tone_hard": "🥊 Жёсткие",
        "btn_tone_mixed": "😈 Очень",

        # Кнопки языков
        "btn_lang_uk": "🇺🇦 Українська",
        "btn_lang_en": "🇬🇧 English",
        "btn_lang_ru": " Рус",

        "share_label": "Публикация медиа в общий чат",
        "btn_share_on": "Вкл 🟢",
        "btn_share_off": "Выкл ⚪",
        "share_updated": "Настройка обновлена",

        # Навигация
        "btn_back": "⬅️ Назад",

        # Сообщения
        "error_invalid_choice": "Неверный выбор",
        "tone_updated": "Стиль уведомлений обновлён ✅",
        "error_invalid_lang": "Неверный язык",
        "lang_updated": "Язык обновлён ✅",

        # Метки текущего языка в шапке
        "lang_badge": {
            "ru": " Рус",
            "uk": "🇺🇦 Українська",
            "en": "🇬🇧 English",
        },
    },
    "uk": {
        "title": "⚙️ Налаштування",
        "description": "Обери стиль сповіщень і мову інтерфейсу.",
        "notification_label": "🔔 Стиль сповіщень",
        "language_label": "🌐 Мова",

        "btn_tone_soft": "🧘 М’які",
        "btn_tone_hard": "🥊 Жорсткі",
        "btn_tone_mixed": "😈 Дуже",

        "btn_lang_uk": "🇺🇦 Українська",
        "btn_lang_en": "🇬🇧 English",
        "btn_lang_ru": " Рус",

        "share_label": "Публікація медіа в загальний чат",
        "btn_share_on": "Увімкн 🟢",
        "btn_share_off": "Вимкн ⚪",
        "share_updated": "Налаштування оновлено",

        "btn_back": "⬅️ Назад",

        "error_invalid_choice": "Неправильний вибір",
        "tone_updated": "Стиль сповіщень оновлено ✅",
        "error_invalid_lang": "Неправильна мова",
        "lang_updated": "Мову оновлено ✅",

        "lang_badge": {
            "ru": " Рус",
            "uk": "🇺🇦 Українська",
            "en": "🇬🇧 English",
        },
    },
    "en": {
        "title": "⚙️ Settings",
        "description": "Choose notification style and interface language.",
        "notification_label": "🔔 Notification style",
        "language_label": "🌐 Language",

        "btn_tone_soft": "🧘 Soft",
        "btn_tone_hard": "🥊 Hard",
        "btn_tone_mixed": "😈 Very",

        "btn_lang_uk": "🇺🇦 Українська",
        "btn_lang_en": "🇬🇧 English",
        "btn_lang_ru": " Рус",

        "share_label": "Share media to public chat",
        "btn_share_on": "On 🟢",
        "btn_share_off": "Off ⚪",
        "share_updated": "Setting updated",

        "btn_back": "⬅️ Back",

        "error_invalid_choice": "Invalid choice",
        "tone_updated": "Notification style updated ✅",
        "error_invalid_lang": "Invalid language",
        "lang_updated": "Language updated ✅",

        "lang_badge": {
            "ru": " Рус",
            "uk": "🇺🇦 Українська",
            "en": "🇬🇧 English",
        },
    },
}
