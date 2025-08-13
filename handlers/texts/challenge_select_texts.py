# ==== ТЕКСТЫ ДЛЯ CHALLENGE_SELECT ====

# Названия уровней челленджей
CHALLENGE_LEVELS = {
    "ru": {
        "level_0": "🔰 Новичок",
        "level_2": "🚶 Основы контроля",
        "level_3": "🧠 Фокус и энергия",
        "level_4": "🔒 Самодисциплина",
        "level_5": "🧱 Преодоление",
        "level_6": "💻 Для будущих предпринимателей",
        "level_7": "⏰ Ранний подъём",
    },
    "uk": {
        "level_0": "🔰 Новачок",
        "level_2": "🚶 Основи контролю",
        "level_3": "🧠 Фокус і енергія",
        "level_4": "🔒 Самодисципліна",
        "level_5": "🧱 Подолання",
        "level_6": "💻 Для майбутніх підприємців",
        "level_7": "⏰ Раннє пробудження",
    },
    "en": {
        "level_0": "🔰 Beginner",
        "level_2": "🚶 Basics of Control",
        "level_3": "🧠 Focus and Energy",
        "level_4": "🔒 Self-Discipline",
        "level_5": "🧱 Overcoming",
        "level_6": "💻 For Future Entrepreneurs",
        "level_7": "⏰ Early Rising",
    },
}

CHALLENGES = {
    "level_0": [
        {
            "id": "cold_shower",
            "ru": ("Контрастный/Холодный душ", "Техники как правильно — <a href=\"https://t.me/c/2370473553/69\">смотри тут</a> \n после просмотра нажми ВЫПОЛНЕНО "),
            "uk": ("Контрастний/Холодний душ", "Техніка правильного обливання — <a href=\"https://t.me/c/2370473553/69\">дивись тут</a> \n після перегляду натисни ВИКОНАНО"),
            "en": ("Contrast/Cold Shower", "Techniques explained — <a href=\"https://t.me/c/2370473553/69\">watch here</a> \n click DONE after watching"),
            "days": 0,
            "type": "view"
        },
        {
            "id": "vessels",
            "ru": ("Прокачка сосудов", "Что бы чувствовать себя хорошо, нужно двигаться — <a href=\"https://t.me/c/2370473553/66\">смотри тут</a>"),
            "uk": ("Прокачка судин", "Щоб добре почуватися, треба рухатись — <a href=\"https://t.me/c/2370473553/66\">дивись тут</a>"),
            "en": ("Vessel Activation", "To feel good — you must move — <a href=\"https://t.me/c/2370473553/66\">watch here</a>"),
            "days": 0,
            "type": "view"
        },
        {
            "id": "hormones",
            "ru": ("Гормоны", "Гормоны управляют настроением — <a href=\"https://t.me/c/2370473553/67\">смотри тут</a>"),
            "uk": ("Гормони", "Гормони керують настроєм — <a href=\"https://t.me/c/2370473553/67\">дивись тут</a>"),
            "en": ("Hormones", "Hormones influence your mood — <a href=\"https://t.me/c/2370473553/67\">watch here</a>"),
            "days": 0,
            "type": "view"
        },
        {
            "id": "start_right",
            "ru": ("Правильно начать", "Не отбей желание раньше времени — <a href=\"https://t.me/c/2370473553/68\">смотри тут</a>"),
            "uk": ("Правильний старт", "Не вбий мотивацію передчасно — <a href=\"https://t.me/c/2370473553/68\">дивись тут</a>"),
            "en": ("Start Right", "Don’t kill motivation too early — <a href=\"https://t.me/c/2370473553/68\">watch here</a>"),
            "days": 0,
            "type": "view"
        },
        {
            "id": "breathing",
            "ru": ("Дыхательная практика", "Плохо дышишь, медленно умираешь — <a href=\"https://t.me/c/2370473553/72\">смотри тут</a>"),
            "uk": ("Дихальна практика", "Погано дихаєш — повільно вмираєш — <a href=\"https://t.me/c/2370473553/72\">дивись тут</a>"),
            "en": ("Breathing Practice", "Bad breathing = slow death — <a href=\"https://t.me/c/2370473553/72\">watch here</a>"),
            "days": 1,
            "type": "media"
        },
        {
            "id": "wake_early",
            "ru": ("Как раньше вставать", "Научись вставать раньше — <a href=\"https://t.me/c/2370473553/74\">смотри тут</a>"),
            "uk": ("Як вставати раніше", "Навчися прокидатися раніше — <a href=\"https://t.me/c/2370473553/74\">дивись тут</a>"),
            "en": ("Wake Up Earlier", "Learn how to wake up earlier — <a href=\"https://t.me/c/2370473553/74\">watch here</a>"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "overcome",
            "ru": ("Почему я не могу побороть себя", "Прокачай лобные доли — <a href=\"https://t.me/c/2370473553/80\">смотри тут</a>"),
            "uk": ("Чому я не можу себе подолати", "Прокачай лобові долі — <a href=\"https://t.me/c/2370473553/80\">дивись тут</a>"),
            "en": ("Why I Can't Overcome Myself", "Train your frontal lobe — <a href=\"https://t.me/c/2370473553/80\">watch here</a>"),
            "days": 1,
            "type": "media"
        },
        {
            "id": "food_brain",
            "ru": ("Еда контролирует наш мозг", "Чем вкуснее питаешься, тем хуже живешь — <a href=\"https://t.me/c/2370473553/81\">смотри тут</a>"),
            "uk": ("Їжа контролює мозок", "Чим смачніше харчуєшся — тим гірше живеш — <a href=\"https://t.me/c/2370473553/81\">дивись тут</a>"),
            "en": ("Food Controls the Brain", "The tastier you eat — the worse you live — <a href=\"https://t.me/c/2370473553/81\">watch here</a>"),
            "days": 1,
            "type": "media"
        }
    ],
    "level_2": [
        {
            "id": "deep_reading",
            "ru": ("30 мин глубокого чтения", "Чтение без отвлечения"),
            "uk": ("30 хв глибокого читання", "Читання без відволікань"),
            "en": ("30 min of deep reading", "Reading without distractions"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "steps_5000",
            "ru": ("5000 шагов", "Пройти минимум 5000 шагов за день"),
            "uk": ("5000 кроків", "Пройти щонайменше 5000 кроків за день"),
            "en": ("5000 steps", "Walk at least 5000 steps a day"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "affirmations",
            "ru": ("Аффирмации", "Повторять свою формулу силы"),
            "uk": ("Афірмації", "Повторюй свою формулу сили"),
            "en": ("Affirmations", "Repeat your personal power phrase"),
            "days": 21,
            "type": "media"
        },
        {
            "id": "no_complaining",
            "ru": ("Без нытья", "Искореняем жалобы и негатив. Я беру ответственность за свою жизнь. Моя жизнь — результат моих же решений. Жалобы — это слабость, а не стратегия."),
            "uk": ("Без ниття", "Викорінюємо скарги та негатив. Я беру відповідальність за своє життя. Моє життя — результат моїх рішень. Скарги — це слабкість, а не стратегія."),
            "en": ("No complaining", "Eliminate complaints and negativity. I take full responsibility for my life. My life is a result of my decisions. Complaining is weakness, not strategy."),
            "days": 30,
            "type": "media"
        },
        {
            "id": "daily_voice_video",
            "ru": ("Кружок каждый день", "Записывать голос/видео что бы переставать стесняться"),
            "uk": ("Кружечок щодня", "Записуй голос або відео, щоб перестати соромитися"),
            "en": ("Daily voice/video post", "Record voice or video daily to stop being shy"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "day_planning",
            "ru": ("Планирование дня", "Записать 3 приоритетные задачи на день \n\nЕсли я не строю план — я становлюсь частью чужого."),
            "uk": ("Планування дня", "Запиши 3 пріоритетні завдання на день \n\nЯкщо я не будую план — я частина чужого."),
            "en": ("Day planning", "Write down 3 priority tasks for the day \n\nIf I don’t build my plan — I become part of someone else’s."),
            "days": 7,
            "type": "media"
        },
        {
            "id": "workout_10_min",
            "ru": ("Тренировка 10 мин", "Минимальная физнагрузка каждый день"),
            "uk": ("Тренування 10 хв", "Мінімальне фізичне навантаження щодня"),
            "en": ("10-min workout", "Minimum physical activity every day"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "reading_10_min",
            "ru": ("Чтение 10 минут", "Читать каждый день хотя бы 10 минут \n\nУбеждения становятся мыслями. Мысли — словами. Слова — действиями. А действия — жизнью."),
            "uk": ("Читання 10 хв", "Читай щодня хоча б 10 хвилин \n\nПереконання стають думками. Думки — словами. Слова — діями. А дії — життям."),
            "en": ("10 minutes of reading", "Read every day for at least 10 minutes \n\nBeliefs become thoughts. Thoughts become words. Words become actions. And actions become life."),
            "days": 21,
            "type": "media"
        },
        {
            "id": "quit_bad_habits",
            "ru": ("Бросаю вредные привычки", "30 дней без алкоголя/никотина/энергетиков"),
            "uk": ("Відмова від шкідливих звичок", "30 днів без алкоголю/нікотину/енергетиків"),
            "en": ("Quit bad habits", "30 days without alcohol/nicotine/energy drinks"),
            "days": 30,
            "type": "media"
        }
    ],
    "level_3": [
        {
            "id": "no_swearing",
            "ru": ("Без мата", "Следить за речью, исключить мат"),
            "uk": ("Без мата", "Стежити за мовленням, виключити лайку"),
            "en": ("No Swearing", "Watch your speech, eliminate swearing"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "no_sugar",
            "ru": ("Без сахара", "Не употреблять сахар в течение дня"),
            "uk": ("Без цукру", "Не вживати цукор протягом дня"),
            "en": ("No Sugar", "Avoid sugar during the day"),
            "days": 21,
            "type": "media"
        },
        {
            "id": "no_fast_food",
            "ru": ("Без фастфуда", "Никакой вредной еды: Макдональдс, шаурма, пицца, бургеры и тд"),
            "uk": ("Без фастфуду", "Ніякої шкідливої їжі: Макдональдс, шаурма, піца, бургери тощо"),
            "en": ("No Fast Food", "No junk food: McDonald’s, shawarma, pizza, burgers, etc."),
            "days": 21,
            "type": "media"
        },
        {
            "id": "meditation",
            "ru": ("Медитация", "Медитировать минимум 5 минут в день"),
            "uk": ("Медитація", "Медитувати мінімум 5 хвилин на день"),
            "en": ("Meditation", "Meditate for at least 5 minutes a day"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "thought_observation",
            "ru": ("Наблюдение за мыслями", "5 мин без реакции на мысли"),
            "uk": ("Спостереження за думками", "5 хв без реакції на думки"),
            "en": ("Thought Observation", "5 minutes of watching thoughts without reacting"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "telegram_post",
            "ru": ("Пост в Telegram", "Писать короткий отчёт или мотивацию"),
            "uk": ("Пост у Telegram", "Писати короткий звіт або мотивацію"),
            "en": ("Telegram Post", "Write a short report or motivational post"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "study",
            "ru": ("Учёба", "30 минут обучения или просмотр курса"),
            "uk": ("Навчання", "30 хвилин навчання або перегляд курсу"),
            "en": ("Study", "30 minutes of learning or course watching"),
            "days": 21,
            "type": "media"
        },
        {
            "id": "barefoot_walk",
            "ru": ("Ходьба босиком", "15 минут босиком"),
            "uk": ("Ходьба босоніж", "15 хвилин босоніж"),
            "en": ("Barefoot Walking", "15 minutes barefoot"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "cold_shower_repeat",
            "ru": ("Холодный душ", "Принимать холодный душ. Техники есть в разделе НОВИЧОК. \n\n Комфорт — это медленная смерть. Выбирай дискомфорт — и будешь расти."),
            "uk": ("Холодний душ", "Приймати холодний душ. Техніки є в розділі НОВАЧКА. \n\n Комфорт — це повільна смерть. Обирай дискомфорт — і будеш зростати."),
            "en": ("Cold Shower", "Take a cold shower. Techniques are in the BEGINNER section. \n\n Comfort is slow death. Choose discomfort — and you’ll grow."),
            "days": 7,
            "type": "media"
        },
        {
            "id": "hour_of_silence",
            "ru": ("Час молчания", "Полное молчание в течение часа"),
            "uk": ("Година мовчання", "Повна тиша протягом години"),
            "en": ("1 Hour of Silence", "Total silence for one hour"),
            "days": 7,
            "type": "media"
        },
        {
            "id": "walk_10_min",
            "ru": ("Прогулка 10 минут", "Выйти на улицу минимум на 10 минут"),
            "uk": ("Прогулянка 10 хвилин", "Вийти на вулицю мінімум на 10 хвилин"),
            "en": ("10-Minute Walk", "Go outside for at least 10 minutes"),
            "days": 7,
            "type": "media"
        }
    ],
    "level_4": [
        {
            "id": "10000_steps",
            "ru": ("10 000 шагов", "Пройти 10 000 шагов за день"),
            "uk": ("10 000 кроків", "Пройти 10 000 кроків за день"),
            "en": ("10,000 steps", "Walk 10,000 steps in a day"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "pullups_10",
            "ru": ("10 подтягиваний", "Сделать 10 подтягиваний подряд"),
            "uk": ("10 підтягувань", "Зробити 10 підтягувань підряд"),
            "en": ("10 pull-ups", "Do 10 pull-ups in a row"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "pushups_50",
            "ru": ("50 отжиманий", "Сделать 50 отжиманий без остановки"),
            "uk": ("50 віджимань", "Зробити 50 віджимань без зупинки"),
            "en": ("50 push-ups", "Do 50 push-ups without stopping"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "run_3km",
            "ru": ("Бег 3 км", "Пробежать минимум 3 км"),
            "uk": ("Біг 3 км", "Пробігти щонайменше 3 км"),
            "en": ("Run 3 km", "Run at least 3 kilometers"),
            "days": 21,
            "type": "media"
        },
        {
            "id": "squats_100",
            "ru": ("100 Приседаний", "100 приседаний в течении дня (можно делить)"),
            "uk": ("100 присідань", "100 присідань протягом дня (можна ділити)"),
            "en": ("100 squats", "100 squats during the day (can be split)"),
            "days": 7,
            "type": "media"
        },
        {
            "id": "cold_shower_voice",
            "ru": ("Холодный душ", "Холодный душ и кружок-реакция"),
            "uk": ("Холодний душ", "Холодний душ + кружечок-реакція"),
            "en": ("Cold shower", "Cold shower + reaction voice"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "digital_detox",
            "ru": ("Цифровой детокс", "Не заходить в соцсети в течение дня \n\n Если я не контролирую внимание — я не контролирую свою жизнь."),
            "uk": ("Цифровий детокс", "Не заходити в соцмережі протягом дня \n\n Якщо я не контролюю увагу — я не контролюю своє життя."),
            "en": ("Digital detox", "Stay off social media all day \n\n If I don’t control my attention — I don’t control my life."),
            "days": 21,
            "type": "media"
        },
        {
            "id": "no_phone_morning",
            "ru": ("Без телефона утром", "Не использовать телефон первые 30 минут"),
            "uk": ("Без телефону зранку", "Не використовувати телефон перші 30 хвилин"),
            "en": ("No phone in the morning", "Don’t use your phone for the first 30 minutes"),
            "days": 7,
            "type": "media"
        },
        {
            "id": "stretch_5min",
            "ru": ("Зарядка 5 минут", "Сделать лёгкую зарядку 5 минут утром"),
            "uk": ("Зарядка 5 хв", "Зробити легку зарядку 5 хвилин зранку"),
            "en": ("5-minute morning stretch", "Light morning stretch for 5 minutes"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "sleep_23",
            "ru": ("Сон до 23:00", "Лечь спать до 23:00"),
            "uk": ("Сон до 23:00", "Лягти спати до 23:00"),
            "en": ("Sleep by 23:00", "Go to bed by 11:00 PM"),
            "days": 21,
            "type": "media"
        }
    ],
    "level_5": [
        {
            "id": "one_meal",
            "ru": ("1 приём пищи в день", "Есть один раз в день"),
            "uk": ("1 прийом їжі на день", "Їсти лише один раз на день"),
            "en": ("One meal a day", "Eat only once a day"),
            "days": 7,
            "type": "media"
        },
        {
            "id": "two_workouts",
            "ru": ("2 тренировки в день", "Две тренировки ежедневно"),
            "uk": ("2 тренування на день", "Два тренування щодня"),
            "en": ("Two workouts a day", "Two workouts daily"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "nofap",
            "ru": ("NoFap", "Полный контроль сексуальных импульсов"),
            "uk": ("NoFap", "Повний контроль сексуальних імпульсів"),
            "en": ("NoFap", "Full control over sexual impulses"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "no_porn",
            "ru": ("Без порно", "Никакого порноконтента"),
            "uk": ("Без порно", "Жодного порноконтенту"),
            "en": ("No porn", "No porn content at all"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "plank",
            "ru": ("Планка", "Делай планку минимум 30 секунд"),
            "uk": ("Планка", "Тримати планку щонайменше 30 секунд"),
            "en": ("Plank", "Hold a plank for at least 30 seconds"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "wake_430",
            "ru": ("Подъём в 4:30", "Просыпаться ровно в 4:30 утра"),
            "uk": ("Пробудження о 4:30", "Прокидатися рівно о 4:30 ранку"),
            "en": ("Wake up at 4:30", "Wake up exactly at 4:30 AM"),
            "days": 21,
            "type": "media"
        },
        {
            "id": "sensory_isolation",
            "ru": ("Сенсорная изоляция", "Никаких звуков, видео, соцсетей"),
            "uk": ("Сенсорна ізоляція", "Жодних звуків, відео, соцмереж"),
            "en": ("Sensory isolation", "No sounds, videos, or social media"),
            "days": 7,
            "type": "media"
        },
        {
            "id": "phone_box",
            "ru": ("Телефон в коробке", "Убирай телефон в ящик/коробку на 2+ часа в день"),
            "uk": ("Телефон у коробці", "Ховай телефон у ящик/коробку на 2+ години"),
            "en": ("Phone in the box", "Put your phone in a box for 2+ hours daily"),
            "days": 14,
            "type": "media"
        },
        {
            "id": "stairs_only",
            "ru": ("Только лестница", "Не пользоваться лифтом — только лестница"),
            "uk": ("Тільки сходи", "Не користуйся ліфтом — тільки сходами"),
            "en": ("Stairs only", "Don’t use the elevator — only stairs"),
            "days": 7,
            "type": "media"
        },
        {
            "id": "focus_2h",
            "ru": ("Фокус 2 часа", "2 часа работы без отвлечений"),
            "uk": ("Фокус 2 години", "2 години безперервної зосередженої роботи"),
            "en": ("2-hour focus", "2 hours of deep, uninterrupted work"),
            "days": 21,
            "type": "media"
        },
        {
            "id": "morning_water",
            "ru": ("Утренняя вода", "Пить стакан воды после пробуждения  \nВода запускает тело, как ключ зажигания запускает мотор."),
            "uk": ("Ранкова вода", "Випий склянку води після пробудження\nВода запускає тіло як ключ — двигун."),
            "en": ("Morning water", "Drink a glass of water after waking up\nWater starts your body like a key starts an engine."),
            "days": 30,
            "type": "media"
        }
    ],
    "level_6": [
        {
            "id": "reading",
            "ru": ("Чтение", "Читать 5 страниц в день"),
            "uk": ("Читання", "Читати 5 сторінок на день"),
            "en": ("Reading", "Read 5 pages a day"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "visualization",
            "ru": ("Визуализация цели", "5 минут представлять свой результат \n\n То что ты можешь представить - ты можешь достичь."),
            "uk": ("Візуалізація цілі", "5 хвилин уявляти свій результат \n\n Те, що можеш уявити — можеш досягти."),
            "en": ("Goal visualization", "Visualize your result for 5 minutes \n\n What you can imagine — you can achieve."),
            "days": 21,
            "type": "media"
        },
        {
            "id": "expenses",
            "ru": ("Учёт расходов", "Записывать все траты за день. \n\nМаленькие утечки топят большие корабли. \nБенджамин Франклин"),
            "uk": ("Облік витрат", "Записуй усі витрати за день \n\nМалі витоки топлять великі кораблі. \nБенджамін Франклін"),
            "en": ("Expense tracking", "Write down all your expenses daily \n\nSmall leaks sink great ships. \nBenjamin Franklin"),
            "days": 30,
            "type": "media"
        },
        {
            "id": "daily_reflection",
            "ru": ("Дневник уроков", "Пиши итоги и ошибки дня в блокнот. Пока я не осознаю свои ошибки, я буду их повторять."),
            "uk": ("Щоденник уроків", "Пиши підсумки та помилки дня в блокнот. Поки я не усвідомлю помилки — я їх повторюю."),
            "en": ("Lessons journal", "Write your daily reflections and mistakes in a notebook. Until I realize my mistakes — I’ll repeat them."),
            "days": 30,
            "type": "media"
        },
        {
            "id": "foreign_words",
            "ru": ("Иностранные языки", "Учить по 5 новых слов (иностр. язык или термины)"),
            "uk": ("Іноземні мови", "Вчи по 5 нових слів (іноземна мова або терміни)"),
            "en": ("Foreign languages", "Learn 5 new words (foreign language or technical terms)"),
            "days": 30,
            "type": "media"
        }
    ],
    "level_7": [
        {
            "id": "wake_7_00",
            "ru": ("Подъем в 7:00", "Подтверждение между 7:00 и 7:04, иначе сброс прогресса"),
            "uk": ("Підйом о 7:00", "Підтвердження між 7:00 та 7:04, інакше скидання прогресу"),
            "en": ("Wake up at 7:00", "Confirm between 7:00 and 7:04, or progress resets"),
            "days": 30,
            "type": "wake_time"
        },
        {
            "id": "wake_6_30",
            "ru": ("Подъем в 6:30", "Подтверждение между 6:30 и 6:34, иначе сброс прогресса"),
            "uk": ("Підйом о 6:30", "Підтвердження між 6:30 та 6:34, інакше скидання прогресу"),
            "en": ("Wake up at 6:30", "Confirm between 6:30 and 6:34, or progress resets"),
            "days": 30,
            "type": "wake_time"
        },
        {
            "id": "wake_6_00",
            "ru": ("Подъем в 6:00", "Подтверждение между 6:00 и 6:04, иначе сброс прогресса"),
            "uk": ("Підйом о 6:00", "Підтвердження між 6:00 та 6:04, інакше скидання прогресу"),
            "en": ("Wake up at 6:00", "Confirm between 6:00 and 6:04, or progress resets"),
            "days": 30,
            "type": "wake_time"
        },
        {
            "id": "wake_5_30",
            "ru": ("Подъем в 5:30", "Подтверждение между 5:30 и 5:34, иначе сброс прогресса"),
            "uk": ("Підйом о 5:30", "Підтвердження між 5:30 та 5:34, інакше скидання прогресу"),
            "en": ("Wake up at 5:30", "Confirm between 5:30 and 5:34, or progress resets"),
            "days": 30,
            "type": "wake_time"
        },
        {
            "id": "wake_5_00",
            "ru": ("Подъем в 5:00", "Подтверждение между 5:00 и 5:04, иначе сброс прогресса"),
            "uk": ("Підйом о 5:00", "Підтвердження між 5:00 та 5:04, інакше скидання прогресу"),
            "en": ("Wake up at 5:00", "Confirm between 5:00 and 5:04, or progress resets"),
            "days": 30,
            "type": "wake_time"
        }
    ]
}

# Челленджи (название, описание, дни, тип)


CHALLENGE_TEXTS = {
    "ru": {
        "back": "⬅️ Назад",
        "back_to_menu": "⬅️ Назад в меню привычек",
        "select_prompt": "Выбирай Брат",
        "bad_request": "⚠️ Telegram выдал ошибку (BadRequest)",
        "load_error": "Произошла ошибка при загрузке меню уровней",
        "challenges_of_level": "🏅 Челленджи уровня {level}",
        "load_failed": "❌ Не удалось загрузить список челленджей.",
        "confirm_challenge": (
            "🔥<b>Активный челлендж:</b>\n\n"
            "<b>Название:</b> {title}\n"
            "<b>Длительность:</b> {days} дней\n"
            "<b>Описание:</b> {desc}\n\n"
            "Добавить в активные привычки?"
        ),
        "take_challenge": "✅ Взять челлендж",
        "already_active": "❌ Этот челлендж уже активен!",
        "added_success": "✅ Челлендж добавлен в активные привычки!",
        "add_failed": "❌ Не удалось добавить челлендж",
        "habit_info": (
            "📌 В привычке ты можешь сам добавить свою привычку.\n"
            "🔥 А в Challenge — выбрать одно из заданий от команды <b>Your Ambitions</b>.\n\n{total}/10"
        ),
        "add_habit": "➕ Добавить привычку",
        "take_from_list": "🔥 Взять Challenge",
        "viewed_button": "✅ Просмотрено",
        "already_viewed": "Уже просмотрено ✅",
        "viewed_success": "✅ {title} отмечено как просмотренное.\nТы получил 1 XP.",
        "too_many_active": "❌ У тебя уже 10 активных привычек или челленджей. Удали одну, чтобы добавить новую."
    },
    "en": {
        "back": "⬅️ Back",
        "back_to_menu": "⬅️ Back to habit menu",
        "select_prompt": "Choose, bro",
        "bad_request": "⚠️ Telegram returned an error (BadRequest)",
        "load_error": "An error occurred while loading level menu",
        "challenges_of_level": "🏅 Challenges of level {level}",
        "load_failed": "❌ Failed to load the list of challenges.",
        "confirm_challenge": (
            "🔥<b>Active Challenge:</b>\n\n"
            "<b>Title:</b> {title}\n"
            "<b>Duration:</b> {days} days\n"
            "<b>Description:</b> {desc}\n\n"
            "Add to active habits?"
        ),
        "take_challenge": "✅ Take challenge",
        "already_active": "❌ This challenge is already active!",
        "added_success": "✅ Challenge added to active habits!",
        "add_failed": "❌ Failed to add challenge",
        "habit_info": (
            "📌 In habits you can create your own task.\n"
            "🔥 In Challenge — choose one of the tasks from the <b>Your Ambitions</b> team.\n\n{total}/10"
        ),
        "add_habit": "➕ Add habit",
        "take_from_list": "🔥 Take Challenge",
        "viewed_button": "✅ Viewed",
        "already_viewed": "Already viewed ✅",
        "viewed_success": "✅ {title} marked as viewed.\nYou received 1 XP.",
        "too_many_active": "❌ You already have 10 active habits or challenges. Delete one to add a new one."
    },
    "uk": {
        "back": "⬅️ Назад",
        "back_to_menu": "⬅️ Назад до меню звичок",
        "select_prompt": "Вибирай, брате",
        "bad_request": "⚠️ Telegram видав помилку (BadRequest)",
        "load_error": "Виникла помилка під час завантаження меню рівнів",
        "challenges_of_level": "🏅 Челенджі рівня {level}",
        "load_failed": "❌ Не вдалося завантажити список челенджів.",
        "confirm_challenge": (
            "🔥<b>Активний челендж:</b>\n\n"
            "<b>Назва:</b> {title}\n"
            "<b>Тривалість:</b> {days} днів\n"
            "<b>Опис:</b> {desc}\n\n"
            "Додати до активних звичок?"
        ),
        "take_challenge": "✅ Взяти челендж",
        "already_active": "❌ Цей челендж вже активний!",
        "added_success": "✅ Челендж додано до активних звичок!",
        "add_failed": "❌ Не вдалося додати челендж",
        "habit_info": (
            "📌 У звичках ти можеш додати власну звичку.\n"
            "🔥 У Challenge — обрати одне із завдань від команди <b>Your Ambitions</b>.\n\n{total}/10"
        ),
        "add_habit": "➕ Додати звичку",
        "take_from_list": "🔥 Взяти Challenge",
        "viewed_button": "✅ Переглянуто",
        "already_viewed": "Вже переглянуто ✅",
        "viewed_success": "✅ {title} відзначено як переглянуте.\nТи отримав 1 XP.",
        "too_many_active": "❌ У тебе вже 10 активних звичок або челенджів. Видали одну, щоб додати нову."
    }
}

