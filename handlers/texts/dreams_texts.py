

#------Главное меню раздела мечт------

DREAMS_MENU_TEXT = {
    "ru": "🎯 Добро пожаловать в раздел силы:",
    "en": "🎯 Welcome to the power section:",
    "ua": "🎯 Ласкаво просимо до розділу сили:"
}

DREAMS_MENU_BUTTONS = {
    "ru": {"goals":"🎯 Цели","plans":"📍 Планы","dreams":"💭 Мечты","hall":"🏆 Зал славы","add":"➕ Добавить"},
    "uk": {"goals":"🎯 Цілі","plans":"📍 Плани","dreams":"💭 Мрії","hall":"🏆 Зала слави","add":"➕ Додати"},
    "en": {"goals":"🎯 Goals","plans":"📍 Plans","dreams":"💭 Dreams","hall":"🏆 Hall of Fame","add":"➕ Add"},
}



#------РАЗДЕЛ ГОАЛС--------

GOALS_VIEW_TEXTS = {
    "ru": {
        "no_goals": "😕 У тебя пока нет целей.\nДобавь новые ➕",
        "title": "🎯 <b>Твои цели:</b>\n\n",
        "status_done": "✅ Завершено",
        "status_active": "🔸 Активно",
        "complete_button": "✅ Завершить цель",
        "delete_button": "🗑 Удалить цель",
        "edit_button": "✏️ Редактировать цель",
        "back_button": "🔙 Назад",
        "goal_completed": "✅ Цель отмечена как завершённая!",
        "goal_completed_alert": "Цель завершена!",
        "choose_goal_to_complete": "Выбери цель, которую хочешь завершить:",
        "no_active_goals": "😕 У тебя пока нет целей.\nДобавь новые ➕",
        "choose_goal_to_delete": "Выбери цель, которую хочешь удалить:",
        "no_goals_to_delete": "😕 У тебя пока нет целей для удаления",
        "goal_deleted": "🗑 Цель удалена.",
        "goal_deleted_alert": "Удалено!",
    },
    "en": {
        "no_goals": "😕 You have no goals yet.\nAdd new ones ➕",
        "title": "🎯 <b>Your Goals:</b>\n\n",
        "status_done": "✅ Completed",
        "status_active": "🔸 Active",
        "complete_button": "✅ Complete Goal",
        "delete_button": "🗑 Delete Goal",
        "edit_button": "✏️ Edit Goal",
        "back_button": "🔙 Back",
        "goal_completed": "✅ Goal marked as completed!",
        "goal_completed_alert": "Goal completed!",
        "choose_goal_to_complete": "Choose a goal to complete:",
        "no_active_goals": "😕 You have no active goals.\nAdd some ➕",
        "choose_goal_to_delete": "Choose a goal to delete:",
        "no_goals_to_delete": "😕 You have no goals to delete",
        "goal_deleted": "🗑 Goal deleted.",
        "goal_deleted_alert": "Deleted!",
    },
    "uk": {
        "no_goals": "😕 У тебе поки немає цілей.\nДодай нові ➕",
        "title": "🎯 <b>Твої цілі:</b>\n\n",
        "status_done": "✅ Завершено",
        "status_active": "🔸 Активна",
        "complete_button": "✅ Завершити ціль",
        "delete_button": "🗑 Видалити ціль",
        "edit_button": "✏️ Редагувати ціль",
        "back_button": "🔙 Назад",
        "goal_completed": "✅ Ціль відзначена як завершена!",
        "goal_completed_alert": "Ціль завершена!",
        "choose_goal_to_complete": "Оберіть ціль для завершення:",
        "no_active_goals": "😕 У тебе поки немає активних цілей.\nДодай нові ➕",
        "choose_goal_to_delete": "Оберіть ціль для видалення:",
        "no_goals_to_delete": "😕 У тебе поки немає цілей для видалення",
        "goal_deleted": "🗑 Ціль видалена.",
        "goal_deleted_alert": "Видалено!",
    }
}


#-----------РАЗДЕЛ ПЛАНОВ----------

# handlers/texts/dreams_texts.py (или другой файл, если ты предпочтешь)
PLANS_VIEW_TEXTS = {
    "ru": {
        "no_plans": "😕 У тебя пока нет планов.\nДобавь новые ➕",
        "title": "📍 <b>Твои планы:</b>\n\n",
        "goal_prefix": "🎯 <b>{goal_title}</b>\n",
        "complete_button": "✅ Выполнено",
        "delete_button": "🗑 Удалить",
        "edit_button": "✏️ Редактировать",
        "back_button": "🔙 Назад",
        "choose_for_complete": "Выбери план для переключения статуса:",
        "no_plans_to_complete": "😕 У тебя пока нет планов для завершения",
        "choose_for_delete": "Выбери план, который хочешь удалить:",
        "no_plans_to_delete": "😕 У тебя пока нет планов для удаления",
        "plan_deleted_last": "🗑<b> План удалён!</b>\n\n <i>Без плана сложнее прийти к тому, чего хочешь. Создай новый!</i>",
        "plan_deleted": "План удалён ✅",
        "plan_not_found": "План не найден.",
    },
    "en": {
        "no_plans": "😕 You don't have any plans yet.\nAdd new ones ➕",
        "title": "📍 <b>Your plans:</b>\n\n",
        "goal_prefix": "🎯 <b>{goal_title}</b>\n",
        "complete_button": "✅ Done",
        "delete_button": "🗑 Delete",
        "edit_button": "✏️ Edit",
        "back_button": "🔙 Back",
        "choose_for_complete": "Choose a plan to toggle its status:",
        "no_plans_to_complete": "😕 You don’t have any plans to complete",
        "choose_for_delete": "Choose a plan you want to delete:",
        "no_plans_to_delete": "😕 You don’t have any plans to delete",
        "plan_deleted_last": "🗑<b> Plan deleted!</b>\n\n <i>Without a plan, it's harder to get where you want. Create a new one!</i>",
        "plan_deleted": "Plan deleted ✅",
        "plan_not_found": "Plan not found.",
    },
    "uk": {
        "no_plans": "😕 У тебе поки немає планів.\nДодай нові ➕",
        "title": "📍 <b>Твої плани:</b>\n\n",
        "goal_prefix": "🎯 <b>{goal_title}</b>\n",
        "complete_button": "✅ Виконано",
        "delete_button": "🗑 Видалити",
        "edit_button": "✏️ Редагувати",
        "back_button": "🔙 Назад",
        "choose_for_complete": "Оберіть план для зміни статусу:",
        "no_plans_to_complete": "😕 У тебе немає планів для завершення",
        "choose_for_delete": "Оберіть план, який хочеш видалити:",
        "no_plans_to_delete": "😕 У тебе немає планів для видалення",
        "plan_deleted_last": "🗑<b> План видалено!</b>\n\n <i>Без плану важко досягти цілі. Створи новий!</i>",
        "plan_deleted": "План видалено ✅",
        "plan_not_found": "План не знайдено.",
    }
}


#---------РАЗДЕЛ МЕЧТ----------

DREAMS_VIEW_TEXTS = {
    "ru": {
        "no_dreams": "😕 У тебя пока нет мечт.\nДобавь новые ➕",
        "actions_prompt": "👇 Действия с мечтой:",
        "dreams_no_photos_title": "<b>💭 Мечты без фото:</b>\n",
        "dreams_no_photos_line": "• {dream_text}\n",
        "no_active_dreams": "Нет активных мечт.",
        "choose_dream_done": "Выбери мечту, которая сбылась:",
        "no_dreams_to_delete": "Нет мечт без фото для удаления.",
        "choose_dream_to_delete": "Выбери мечту, которую хочешь удалить:",
        "dream_deleted": "🗑 Мечта удалена.",
        "confirm_delete": "Ты уверен, что хочешь удалить мечту с фото?",
        "dream_deleted_with_photos": "🗑 Мечта с фото успешно удалена.",
        "dream_done": (
            "💭 <b>Твоя мечта добавлена в Зал Славы!</b>\n\n"
            "✨ <i>Это твой путь, друг. Твои мечты будут храниться там! \n Горжусь тобой</i>"
        ),
        "buttons": {
            "dream_done": "✨ Мечта сбылась",
            "delete": "🗑 Удалить",
            "add_photo": "📷 Добавить фото",
            "back": "🔙 Назад",
            "yes": "✅ Да",
            "no": "🔙 Нет",
        },
    },
    "en": {
        "no_dreams": "😕 You don't have any dreams yet.\nAdd new ones ➕",
        "actions_prompt": "👇 Actions with the dream:",
        "dreams_no_photos_title": "<b>💭 Dreams without photos:</b>\n",
        "dreams_no_photos_line": "• {dream_text}\n",
        "no_active_dreams": "No active dreams.",
        "choose_dream_done": "Choose a dream that came true:",
        "no_dreams_to_delete": "No dreams without photos to delete.",
        "choose_dream_to_delete": "Choose a dream you want to delete:",
        "dream_deleted": "🗑 Dream deleted.",
        "confirm_delete": "Are you sure you want to delete the dream with photos?",
        "dream_deleted_with_photos": "🗑 Dream with photos successfully deleted.",
        "dream_done": (
            "💭 <b>Your dream was added to the Hall of Fame!</b>\n\n"
            "✨ <i>This is your path, friend. Your dreams will be stored there! \n I'm proud of you</i>"
        ),
        "buttons": {
            "dream_done": "✨ Dream came true",
            "delete": "🗑 Delete",
            "add_photo": "📷 Add photo",
            "back": "🔙 Back",
            "yes": "✅ Yes",
            "no": "🔙 No",
        },
    },
    "uk": {
        "no_dreams": "😕 У тебе поки немає мрій.\nДодай нові ➕",
        "actions_prompt": "👇 Дії з мрією:",
        "dreams_no_photos_title": "<b>💭 Мрії без фото:</b>\n",
        "dreams_no_photos_line": "• {dream_text}\n",
        "no_active_dreams": "Немає активних мрій.",
        "choose_dream_done": "Оберіть мрію, яка здійснилася:",
        "no_dreams_to_delete": "Немає мрій без фото для видалення.",
        "choose_dream_to_delete": "Оберіть мрію, яку хочеш видалити:",
        "dream_deleted": "🗑 Мрію видалено.",
        "confirm_delete": "Ти впевнений, що хочеш видалити мрію з фото?",
        "dream_deleted_with_photos": "🗑 Мрію з фото успішно видалено.",
        "dream_done": (
            "💭 <b>Твоя мрія додана до Залу Слави!</b>\n\n"
            "✨ <i>Це твій шлях, друже. Твої мрії будуть зберігатися там! \n Я пишаюсь тобою</i>"
        ),
        "buttons": {
            "dream_done": "✨ Мрія здійснилась",
            "delete": "🗑 Видалити",
            "add_photo": "📷 Додати фото",
            "back": "🔙 Назад",
            "yes": "✅ Так",
            "no": "🔙 Ні",
        },
    }
}



#----------Добавление ФОТО ФСМ----------



DREAMS_ADD_PHOTO_FSM_TEXTS = {
    "ru": {
        "error_loading_dreams": "Ошибка при загрузке мечт.",
        "no_active_dreams": "У тебя пока нет активных мечт.",
        "select_dream_prompt": "Выбери мечту, к которой хочешь добавить фото:",
        "cancel_button": "🚫 Отмена",
        "send_photo_prompt": "📷 Отправь фото для этой мечты (до 3 штук).",
        "photo_save_error": "❌ Не удалось сохранить фото.",
        "photo_limit": "⚠️ У этой мечты уже 3 фото. Удали старое, чтобы добавить новое.",
        "photo_success": "✅ Фото успешно добавлено!",
        "cancel_success": "❌ Добавление фото отменено."
    },
    "en": {
        "error_loading_dreams": "Error loading dreams.",
        "no_active_dreams": "You have no active dreams yet.",
        "select_dream_prompt": "Choose a dream to add a photo:",
        "cancel_button": "🚫 Cancel",
        "send_photo_prompt": "📷 Send a photo for this dream (up to 3).",
        "photo_save_error": "❌ Failed to save photo.",
        "photo_limit": "⚠️ This dream already has 3 photos. Delete an old one to add new.",
        "photo_success": "✅ Photo added successfully!",
        "cancel_success": "❌ Photo addition cancelled."
    },
    "uk": {
        "error_loading_dreams": "Помилка при завантаженні мрій.",
        "no_active_dreams": "У тебе поки немає активних мрій.",
        "select_dream_prompt": "Вибери мрію, до якої хочеш додати фото:",
        "cancel_button": "🚫 Скасувати",
        "send_photo_prompt": "📷 Надішли фото для цієї мрії (до 3 штук).",
        "photo_save_error": "❌ Не вдалося зберегти фото.",
        "photo_limit": "⚠️ У цієї мрії вже 3 фото. Видали старе, щоб додати нове.",
        "photo_success": "✅ Фото успішно додано!",
        "cancel_success": "❌ Додавання фото скасовано."
    }
}



#----------ЗАЛ СЛАВЫ----------

HALLS_TEXTS = {
    "ru": {
        "empty": "😕 У тебя пока пусто в Зале Славы...",
        "title": "🏆 <b>Зал Славы:</b>\n\n",
        "completed_goals_title": "<b>🎯 Завершённые цели:</b>\n",
        "goal_line": "✅ {text}\n📅 {from_date} → {to_date}\n\n",
        "completed_dreams_title": "<b>💭 Исполненные мечты:</b>\n",
        "dream_line": "💭 {text}\n📅 {from_date} → {to_date}\n\n",
        "back_menu_title": "🎯 Добро пожаловать в раздел силы:",
        "buttons": {
            "goals": "🎯 Мои цели",
            "plans": "📍 Мои планы",
            "dreams": "💭 Мои мечты",
            "hall": "🏆 Зал славы",
            "add": "➕ Добавить новую"
        },
        "dream_done": (
            "💭 <b>Твоя мечта добавлена в Зал Славы!</b>\n\n"
            "✨ <i>Это твой путь, друг. Твои мечты будут храниться там! \n Горжусь тобой</i>"
        )
    },
    "en": {
        "empty": "😕 Your Hall of Fame is still empty...",
        "title": "🏆 <b>Hall of Fame:</b>\n\n",
        "completed_goals_title": "<b>🎯 Completed Goals:</b>\n",
        "goal_line": "✅ {text}\n📅 {from_date} → {to_date}\n\n",
        "completed_dreams_title": "<b>💭 Fulfilled Dreams:</b>\n",
        "dream_line": "💭 {text}\n📅 {from_date} → {to_date}\n\n",
        "back_menu_title": "🎯 Welcome to the Power Section:",
        "buttons": {
            "goals": "🎯 My Goals",
            "plans": "📍 My Plans",
            "dreams": "💭 My Dreams",
            "hall": "🏆 Hall of Fame",
            "add": "➕ Add New"
        },
        "dream_done": (
            "💭 <b>Your dream has been added to the Hall of Fame!</b>\n\n"
            "✨ <i>This is your path, my friend. Your dreams are stored there! I'm proud of you</i>"
        )
    },
    "uk": {
        "empty": "😕 У тебе поки що порожньо в Залі Слави...",
        "title": "🏆 <b>Зал Слави:</b>\n\n",
        "completed_goals_title": "<b>🎯 Завершені цілі:</b>\n",
        "goal_line": "✅ {text}\n📅 {from_date} → {to_date}\n\n",
        "completed_dreams_title": "<b>💭 Здійснені мрії:</b>\n",
        "dream_line": "💭 {text}\n📅 {from_date} → {to_date}\n\n",
        "back_menu_title": "🎯 Ласкаво просимо до розділу сили:",
        "buttons": {
            "goals": "🎯 Мої цілі",
            "plans": "📍 Мої плани",
            "dreams": "💭 Мої мрії",
            "hall": "🏆 Зал слави",
            "add": "➕ Додати нову"
        },
        "dream_done": (
            "💭 <b>Твоя мрія додана до Залу Слави!</b>\n\n"
            "✨ <i>Це твій шлях, друже. Твої мрії зберігаються там! Пишаюся тобою</i>"
        )
    }
}




#----------ДОБАВЛЕНИЕ ЦЕЛЕЙ ПЛАНОВ МЕЧТ----------



FSM_ADD_TEXTS = {
    "ru": {
        "choose_what_to_add": "➕ Что ты хочешь добавить?",
        "goal_button": "🎯 Цель",
        "plan_button": "📍 План",
        "dream_button": "💭 Мечту",
        "back_button": "🔙 Назад",

        "ask_goal_text": "✍️ Введи текст цели:",
        "empty_goal_error": "❗ Цель не может быть пустой. Попробуй ещё раз:",
        "goal_added": "🎯 Цель добавлена:\n<b>{text}</b>",
        "goal_save_error": "❌ Ошибка при сохранении цели.",

        "ask_dream_text": "💭 Введи свою мечту:",
        "empty_dream_error": "❗ Мечта не может быть пустой. Попробуй ещё раз:",
        "dream_added": "💭 Мечта добавлена:\n<b>{text}</b>",
        "dream_save_error": "❌ Ошибка при сохранении мечты.",

        "ask_plan_binding": "❓ Хочешь привязать план к цели?",
        "bind_yes": "✅ Да, выбрать цель",
        "bind_no": "❌ Нет, просто добавить",

        "choose_goal_to_bind": "Выбери цель, к которой привязать план:",
        "ask_plan_text": "✍️ Введи текст плана:",
        "empty_plan_error": "❗ План не может быть пустым. Попробуй ещё раз:",
        "plan_added_linked": "📍 План добавлен!\nПривязан к цели ✅",
        "plan_added_unlinked": "📍 План добавлен!\nБез привязки ❌",
        "plan_save_error": "❌ Ошибка при сохранении плана.",

        "choose_goal_to_edit": "Выбери цель для редактирования:",
        "choose_plan_to_edit": "Выбери план для редактирования:",
        "no_goals_to_edit": "😕 У тебя пока нет целей для редактирования",
        "no_plans_to_edit": "😕 У тебя пока нет планов для редактирования.",

        "ask_new_goal_text": "✍️ Введи новый текст для цели:",
        "goal_updated": "✅ Цель обновлена!",

        "ask_new_plan_text": "✍️ Введи новый текст плана:",
        "plan_updated": "✅ План успешно отредактирован!",

        "empty_text_error": "❗ Текст не может быть пустым. Попробуй снова:",

        "cancel_text": "❌ Добавление отменено.",
        "cancel_button": "❌ Отмена"
    },

    "uk": {
        "choose_what_to_add": "➕ Що ти хочеш додати?",
        "goal_button": "🎯 Ціль",
        "plan_button": "📍 План",
        "dream_button": "💭 Мрію",
        "back_button": "🔙 Назад",

        "ask_goal_text": "✍️ Введи текст цілі:",
        "empty_goal_error": "❗ Ціль не може бути порожньою. Спробуй ще раз:",
        "goal_added": "🎯 Ціль додано:\n<b>{text}</b>",
        "goal_save_error": "❌ Помилка при збереженні цілі.",

        "ask_dream_text": "💭 Введи свою мрію:",
        "empty_dream_error": "❗ Мрія не може бути порожньою. Спробуй ще раз:",
        "dream_added": "💭 Мрію додано:\n<b>{text}</b>",
        "dream_save_error": "❌ Помилка при збереженні мрії.",

        "ask_plan_binding": "❓ Хочеш прив'язати план до цілі?",
        "bind_yes": "✅ Так, обрати ціль",
        "bind_no": "❌ Ні, просто додати",

        "choose_goal_to_bind": "Вибери ціль, до якої прив'язати план:",
        "ask_plan_text": "✍️ Введи текст плану:",
        "empty_plan_error": "❗ План не може бути порожнім. Спробуй ще раз:",
        "plan_added_linked": "📍 План додано!\nПрив'язано до цілі ✅",
        "plan_added_unlinked": "📍 План додано!\nБез прив'язки ❌",
        "plan_save_error": "❌ Помилка при збереженні плану.",

        "choose_goal_to_edit": "Вибери ціль для редагування:",
        "choose_plan_to_edit": "Вибери план для редагування:",
        "no_goals_to_edit": "😕 У тебе ще немає цілей для редагування",
        "no_plans_to_edit": "😕 У тебе ще немає планів для редагування.",

        "ask_new_goal_text": "✍️ Введи новий текст для цілі:",
        "goal_updated": "✅ Ціль оновлено!",

        "ask_new_plan_text": "✍️ Введи новий текст плану:",
        "plan_updated": "✅ План успішно відредаговано!",

        "empty_text_error": "❗ Текст не може бути порожнім. Спробуй знову:",

        "cancel_text": "❌ Додавання скасовано.",
        "cancel_button": "❌ Скасувати"
    },

    "en": {
        "choose_what_to_add": "➕ What do you want to add?",
        "goal_button": "🎯 Goal",
        "plan_button": "📍 Plan",
        "dream_button": "💭 Dream",
        "back_button": "🔙 Back",

        "ask_goal_text": "✍️ Enter your goal:",
        "empty_goal_error": "❗ The goal cannot be empty. Try again:",
        "goal_added": "🎯 Goal added:\n<b>{text}</b>",
        "goal_save_error": "❌ Error saving the goal.",

        "ask_dream_text": "💭 Enter your dream:",
        "empty_dream_error": "❗ The dream cannot be empty. Try again:",
        "dream_added": "💭 Dream added:\n<b>{text}</b>",
        "dream_save_error": "❌ Error saving the dream.",

        "ask_plan_binding": "❓ Do you want to link the plan to a goal?",
        "bind_yes": "✅ Yes, choose a goal",
        "bind_no": "❌ No, just add",

        "choose_goal_to_bind": "Choose a goal to link the plan to:",
        "ask_plan_text": "✍️ Enter the plan text:",
        "empty_plan_error": "❗ The plan cannot be empty. Try again:",
        "plan_added_linked": "📍 Plan added!\nLinked to a goal ✅",
        "plan_added_unlinked": "📍 Plan added!\nNo link ❌",
        "plan_save_error": "❌ Error saving the plan.",

        "choose_goal_to_edit": "Choose a goal to edit:",
        "choose_plan_to_edit": "Choose a plan to edit:",
        "no_goals_to_edit": "😕 You have no goals to edit yet",
        "no_plans_to_edit": "😕 You have no plans to edit yet.",

        "ask_new_goal_text": "✍️ Enter the new goal text:",
        "goal_updated": "✅ Goal updated!",

        "ask_new_plan_text": "✍️ Enter the new plan text:",
        "plan_updated": "✅ Plan successfully updated!",

        "empty_text_error": "❗ Text cannot be empty. Try again:",

        "cancel_text": "❌ Addition canceled.",
        "cancel_button": "❌ Cancel"
    }
}

