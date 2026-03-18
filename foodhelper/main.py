import os
import telebot
from telebot import types 
from gigachat import GigaChat
import time
from telebot import types, apihelper

# ==========================================
# ⚙️ НАСТРОЙКИ И ТОКЕНЫ
# ==========================================
# 1. Токен от BotFather
TELEGRAM_BOT_TOKEN = '8302119545:AAHjv1D-XeI9SRe6GJOpVTKoRb_kAe1aihQ'

# 2. Токен от GigaChat
GIGACHAT_CREDENTIALS = 'MDE5YWU5ZmMtODZkNi03MmNjLTg4NjktZWJjZDlmNTc4M2VhOjk5MWIxNWQ5LTA0OTMtNGQ0ZS04ZjY2LWY2YjQ1NTk3ZDAyZg=='

# 3. Режим демонстрации (без реальных запросов к GigaChat, для тестов и отладки)
DEMO_MODE = False

apihelper.proxy = {'https': 'http://Edfk1t:X2a09U@185.192.1.206:8000'}

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ==========================================
# 🌍 ЛОКАЛИЗАЦИЯ (MESSAGES)
# ==========================================
MESSAGES = {
    'ru': {
        'default_basic': "вода, соль, перец, сахар, растительное масло",
        'choose_lang': "🌍 Выберите язык / Choose language:",
        
        # Приветственное сообщение
        'welcome_text': "Добро пожаловать на кухню! 🔪\nЯ ваш личный кулинарный ИИ-помощник. Мои главные навыки:\n🥕 Придумаю рецепт строго из ваших продуктов.\n📖 Расскажу, как приготовить любое известное блюдо.\n🧂 Запомню ваши базовые продукты, чтобы не вводить их каждый раз.",
        
        # Главное меню
        'menu_text': "🏠 **Главное меню**\nВыберите действие:",
        'btn_menu_ing': "🥕 Поиск по ингредиентам",
        'btn_menu_dish': "📖 Поиск по готовому блюду",
        'btn_menu_basic': "🧂 Сменить базовые продукты",
        'btn_menu_lang': "🌍 Сменить язык",
        
        # Настройки базовых продуктов
        'basic_info': "🧂 **Ваши базовые продукты:**\n_{basic}_\n\nЧто хотите сделать?",
        'btn_keep': "✅ Готово / Назад",
        'btn_overwrite': "🔄 Заменить список", 
        'btn_add': "➕ Добавить продукты",
        
        'ask_overwrite': "🗑 Старый список будет удален.\n✍️ Напишите **новый** полный список базовых продуктов:",
        'ask_add': "✍️ Напишите продукты, которые нужно **добавить** к списку:",
        'basic_updated': "✅ **Список обновлен!**\nТекущие запасы: _{basic}_",
        'not_basic_products': "⛔️ **Это не похоже на продукты.**\nПопробуйте еще раз.",
        
        # Ввод данных
        'ask_ing': "🥕 **Поиск по ингредиентам**\nНапишите список продуктов, которые у вас есть (например: `курица, картошка`).",
        'ask_dish': "📖 **Поиск по блюду**\nНапишите название блюда, которое хотите приготовить (например: `Лазанья`).",
        
        # Статусы и сообщения
        'history_empty': "История пуста.",
        'searching': "Ищу новый вариант...",
        'checking': "🧐 Шеф проверяет данные...",
        'analyzing_methods': "🤔 Думаю, на чем это лучше приготовить...",
        'choose_method': "🔥 **На чем будем готовить?**\nВыберите доступный прибор или нажмите 'Любой способ':",
        'thinking': "👨‍🍳 Шеф составляет рецепт...",
        'bonus_found': "💡 **Идея от Шефа!**\n\nЕсли добавить всего один продукт — **{ing}**, можно приготовить:\n🍛 **{dish}**",
        'bon_appetit': "Приятного аппетита! 👨‍🍳",
        
        # Ошибки валидации
        'not_products': "⛔️ **Это не похоже на список продуктов.**\nПожалуйста, введите только съедобные ингредиенты.",
        'not_dish': "⛔️ **Это не похоже на название блюда.**\nПожалуйста, напишите корректное название (например: `Борщ`, `Пицца`).",
        
        # Кнопки действий с рецептом
        'btn_regen': "🔄 Другой вариант",
        'btn_lang': "🌍 Сменить язык",
        'btn_get_bonus': "📖 Рецепт: {dish}",
        'btn_menu': "🏠 В меню",
        'btn_method_any': "🤷 Любой способ",
        
        'link_yandex': "🖼 Посмотреть фото в Яндексе",
        'dish_fallback': "Вкусная еда"
    },
    'en': {
        'default_basic': "water, salt, pepper, sugar, vegetable oil",
        'choose_lang': "🌍 Choose language / Выберите язык:",
        
        # Welcome
        'welcome_text': "Welcome to the kitchen! 🔪\nI am your personal culinary AI assistant. My main skills:\n🥕 Invent a recipe strictly from your products.\n📖 Tell you how to cook any known dish.\n🧂 Remember your basic products so you don't have to enter them every time.",
        
        # Main Menu
        'menu_text': "🏠 **Main Menu**\nChoose an action:",
        'btn_menu_ing': "🥕 Search by Ingredients",
        'btn_menu_dish': "📖 Search by Dish Name",
        'btn_menu_basic': "🧂 Change Basic Ingredients",
        'btn_menu_lang': "🌍 Change Language",
        
        # Settings
        'basic_info': "🧂 **Your basic ingredients:**\n_{basic}_\n\nWhat would you like to do?",
        'btn_keep': "✅ Done / Back",
        'btn_overwrite': "🔄 Replace List",
        'btn_add': "➕ Add Ingredients",
        
        'ask_overwrite': "🗑 Old list will be deleted.\n✍️ Write a **new** complete list of basic ingredients:",
        'ask_add': "✍️ Write ingredients to **add** to the current list:",
        'basic_updated': "✅ **List updated!**\nCurrent items: _{basic}_",
        'not_basic_products': "⛔️ **This doesn't look like food.**\nTry again.",
        
        # Inputs
        'ask_ing': "🥕 **Search by Ingredients**\nWrite ingredients you have (e.g., `chicken, potato`).",
        'ask_dish': "📖 **Search by Dish Name**\nWrite the name of the dish (e.g., `Lasagna`).",

        # Statuses
        'history_empty': "History is empty.",
        'searching': "Looking for a new option...",
        'checking': "🧐 Chef is checking data...",
        'analyzing_methods': "🤔 Thinking about cooking methods...",
        'choose_method': "🔥 **How should we cook this?**\nChoose an appliance or click 'Any method':",
        'thinking': "👨‍🍳 Chef is creating a recipe...",
        'bonus_found': "💡 **Chef's Tip!**\n\nIf you add just one ingredient — **{ing}**, you can cook:\n🍛 **{dish}**",
        'bon_appetit': "Bon appetit! 👨‍🍳",
        
        # Errors
        'not_products': "⛔️ **Found non-edible items or nonsense.**\nPlease enter ONLY food ingredients.",
        'not_dish': "⛔️ **This doesn't look like a dish name.**\nPlease write a valid dish name (e.g., `Soup`, `Pizza`).",
        
        # Buttons
        'btn_regen': "🔄 Another variant",
        'btn_lang': "🌍 Change Language",
        'btn_get_bonus': "📖 Recipe: {dish}",
        'btn_menu': "🏠 Main Menu",
        'btn_method_any': "🤷 Any method",
        
        'link_yandex': "🖼 View photo in Yandex",
        'dish_fallback': "Delicious food"
    }
}

# ==========================================
# 💾 ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ
# ==========================================
user_last_ingredients = {}
user_selected_method = {}
user_basic_ingredients = {}
user_language = {}
user_mode = {}
user_state = {}
user_bonus_ingredient = {}
user_target_dish = {}

# ==========================================
# 🛠 ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def get_lang(chat_id):
    return user_language.get(chat_id, 'ru')

def get_mode(chat_id):
    return user_mode.get(chat_id, 'normal')

def get_msg(chat_id, key, **kwargs):
    lang = get_lang(chat_id)
    text = MESSAGES[lang].get(key, MESSAGES['ru'].get(key, f"Error: {key}"))
    if kwargs:
        return text.format(**kwargs)
    return text

# ==========================================
# 🤖 API GIGACHAT
# ==========================================

def get_gigachat_response(prompt):
    if DEMO_MODE:
        time.sleep(1.5)
        if "абракадабра" in prompt.lower(): return "ОШИБКА"
        if "способ" in prompt.lower(): return "Духовка, Сковорода, Мультиварка"
        if "дополнительный" in prompt.lower(): return "Сыр|Пицца"
        return get_mock_text_response()

    if GIGACHAT_CREDENTIALS == 'YOUR_GIGACHAT_AUTH_KEY_HERE':
        return "⚠️ Ошибка: Вы не вставили ключ GigaChat в код!"

    try:
        with GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False) as giga:
            response = giga.chat(prompt)
            return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка GigaChat: {e}")
        return f"ОШИБКА_API"

def get_mock_text_response():
    return "🍽 **Блюдо Демонстрационное**\n\n⏱ 5 мин\n🔪 Смешайте всё."

# ==========================================
# ⌨️ UI КЛАВИАТУРЫ
# ==========================================

def create_main_menu_keyboard(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_ing = types.KeyboardButton(get_msg(chat_id, 'btn_menu_ing'))
    btn_dish = types.KeyboardButton(get_msg(chat_id, 'btn_menu_dish'))
    btn_basic = types.KeyboardButton(get_msg(chat_id, 'btn_menu_basic'))
    btn_lang = types.KeyboardButton(get_msg(chat_id, 'btn_menu_lang'))
    markup.add(btn_ing, btn_dish, btn_basic, btn_lang)
    return markup

def create_basic_setup_keyboard(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_keep = types.KeyboardButton(get_msg(chat_id, 'btn_keep'))
    btn_overwrite = types.KeyboardButton(get_msg(chat_id, 'btn_overwrite'))
    btn_add = types.KeyboardButton(get_msg(chat_id, 'btn_add'))
    markup.add(btn_add, btn_overwrite)
    markup.add(btn_keep)
    return markup

# ==========================================
# 📝 ПРОМПТЫ (ИНСТРУКЦИИ ДЛЯ ИИ)
# ==========================================

def make_validation_prompt(ingredients, lang='ru'):
    if lang == 'ru':
        return (
            f"Проверь текст: '{ingredients}'. "
            f"Если это съедобные продукты питания, выведи ровно одно слово: ПРОДУКТЫ. "
            f"Если это несъедобные предметы, техника, абстракция или бессмыслица, выведи ровно одно слово: ОШИБКА. "
            f"Не пиши больше ничего."
        )
    return f"Analyze: '{ingredients}'. Answer STRICTLY with one word: FOOD if all items are edible. Answer ERROR if there is any non-edible object or nonsense."

def make_dish_validation_prompt(dish_name, lang='ru'):
    if lang == 'ru':
        return (
            f"Проверь текст: '{dish_name}'. Является ли это названием кулинарного блюда? "
            f"Выведи ровно одно слово: ПРОДУКТЫ, если это еда. "
            f"Выведи ровно одно слово: ОШИБКА, если это несъедобный предмет, техника или бессмыслица. "
            f"Не пиши больше ничего."
        )
    return f"Analyze: '{dish_name}'. Is this a real food or dish name? Answer STRICTLY with one word: FOOD if it's edible. Answer ERROR if it's a vehicle, tool, abstract concept, or nonsense."

def make_methods_prompt(input_text, lang='ru'):
    if lang == 'ru':
        return (
            f"Пользователь хочет приготовить: '{input_text}'. "
            f"Выбери 2-4 способа ТЕРМИЧЕСКОЙ обработки ИСКЛЮЧИТЕЛЬНО из: [Сковорода, Кастрюля, Духовка, Микроволновка, Мультиварка, Пароварка, Гриль, Костер]. "
            f"НЕ предлагай инструменты типа ножа, терки или формы для запекания. Только приборы для нагрева. "
            f"Ответь СТРОГО словами через запятую. Не пиши 'Список:' или другие вводные слова."
        )
    return (
        f"User wants to cook: '{input_text}'. "
        f"Select 2-4 THERMAL cooking methods STRICTLY from: [Frying Pan, Pot, Oven, Microwave, Multicooker, Steamer, Grill, Campfire]. "
        f"DO NOT suggest tools like knives, peelers or bowls. Only appliances that heat food. "
        f"Answer STRICTLY with comma-separated words. Do not write 'List:' or intro text."
    )

def get_strict_constraints(method, lang='ru'):
    method_lower = method.lower()
    constraints = []
    
    if "любой" in method_lower or "any" in method_lower:
        return "" 

    if lang == 'ru':
        if 'микроволн' in method_lower or 'свч' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать плиту, кастрюли, сковороды, духовку. Все готовить ВНУТРИ микроволновки.")
        elif 'духовк' in method_lower or 'печь' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать конфорки, сковороды или кастрюли. Все готовить ВНУТРИ духовки.")
        elif 'гриль' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать сковороду, кастрюлю, духовку или микроволновку. Готовить ИСКЛЮЧИТЕЛЬНО на гриле (на решетке).")
        elif 'сковород' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать духовку, гриль или микроволновку. Готовить ТОЛЬКО на плите в сковороде.")
        elif 'кастрюл' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать духовку, сковороду или гриль. Готовить ТОЛЬКО в кастрюле.")
        elif 'мультиварк' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать духовку, плиту, сковороды. Готовить ТОЛЬКО в чаше мультиварки.")
        elif 'костер' in method_lower or 'костр' in method_lower:
            constraints.append("СТРОЖАЙШИЙ ЗАПРЕТ: Нельзя использовать домашнюю плиту, духовку, микроволновку. Готовить только на костре (на шампурах, в казане или фольге).")
    else:
        if 'microwave' in method_lower:
            constraints.append("STRICT BAN: Do NOT use stove, pots, pans. Cook INSIDE microwave.")
        elif 'grill' in method_lower:
            constraints.append("STRICT BAN: Do NOT use pans, pots, or oven. Cook ONLY on the grill.")
    
    return " ".join(constraints) if constraints else ""

def make_recipe_prompt(ingredients, basic_ingredients, method, lang='ru', is_retry=False):
    strict_rules = get_strict_constraints(method, lang)
    if lang == 'ru':
        retry_text = "Придумай ДРУГОЙ рецепт." if is_retry else "Придумай рецепт."
        prompt = (
            f"Ты строгий шеф-повар. Готовь ТОЛЬКО из: {ingredients}. База: {basic_ingredients}. "
            f"Способ: {method}. {strict_rules} "
            f"КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО добавлять продукты (мясо, овощи, яйца, муку), если их нет в списке. "
            f"ВНИМАТЕЛЬНО ПРОЧИТАЙ СПОСОБ И ЗАПРЕТЫ И НЕ НАРУШАЙ ИХ. "
            f"{retry_text} "
            f"Ответь на РУССКОМ языке ОБЯЗАТЕЛЬНО по формату:\n"
            f"🍽 **Название**\n\n⏱ **Время:** ... | 📊 **Сложность:** ...\n"
            f"🔥 **Ккал:** ... | 🥩 **Б:** ... | 🧈 **Ж:** ... | 🍞 **У:** ...\n\n"
            f"🛒 **Ингредиенты:**\n(только из списка)\n\n🔪 **Инструкция:**\n...\n\n💡 **Совет:** ..."
        )
    else:
        retry_text = "Invent ANOTHER recipe." if is_retry else "Invent a recipe."
        prompt = (
            f"Strict chef. Use ONLY: {ingredients}. Basic: {basic_ingredients}. Method: {method}. {strict_rules} "
            f"FORBIDDEN to add unlisted products. READ THE CONSTRAINTS CAREFULLY. {retry_text} "
            f"Answer in ENGLISH following format:\n"
            f"🍽 **Dish Name**\n\n⏱ **Time:** ...\n🔥 **Kcal:** ...\n\n🛒 **Ingredients:**\n...\n\n🔪 **Instructions:**\n..."
        )
    return prompt

def make_reverse_recipe_prompt(dish_name, method, lang='ru'):
    strict_rules = get_strict_constraints(method, lang)
    if lang == 'ru':
        prompt = (
            f"Шеф-повар. Блюдо: '{dish_name}'. Способ: {method}. {strict_rules} "
            f"Напиши классический рецепт. МОЖЕШЬ использовать любые продукты. "
            f"Ответь на РУССКОМ языке по формату:\n"
            f"🍽 **Название**\n\n⏱ **Время:** ...\n🔥 **Ккал:** ...\n\n🛒 **Ингредиенты:**\n...\n\n🔪 **Инструкция:**\n..."
        )
    else:
        prompt = (
            f"Chef. Dish: '{dish_name}'. Method: {method}. {strict_rules} "
            f"Write classic recipe. Any ingredients allowed. Answer in ENGLISH standard format."
        )
    return prompt

def make_bonus_recipe_prompt(ingredients, basic_ingredients, dish_name, method, lang='ru'):
    strict_rules = get_strict_constraints(method, lang)
    if lang == 'ru':
        prompt = (
            f"Ты строгий шеф-повар. Твоя задача: приготовить блюдо '{dish_name}'. "
            f"У пользователя есть ТОЛЬКО эти продукты: {ingredients}. База: {basic_ingredients}. "
            f"Способ: {method}. {strict_rules} "
            f"КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО добавлять другие продукты (никакого лишнего мяса, овощей, соусов, если их нет в списке). "
            f"Ответь на РУССКОМ языке ОБЯЗАТЕЛЬНО по формату:\n"
            f"🍽 **Название**\n\n⏱ **Время:** ... | 📊 **Сложность:** ...\n"
            f"🔥 **Ккал:** ... | 🥩 **Б:** ... | 🧈 **Ж:** ... | 🍞 **У:** ...\n\n"
            f"🛒 **Ингредиенты:**\n(только из списка)\n\n🔪 **Инструкция:**\n...\n\n💡 **Совет:** ..."
        )
    else:
        prompt = (
            f"Strict chef. Target dish: '{dish_name}'. "
            f"Use ONLY these products: {ingredients}. Basic: {basic_ingredients}. "
            f"Method: {method}. {strict_rules} "
            f"FORBIDDEN to add unlisted products. "
            f"Answer in ENGLISH following format:\n"
            f"🍽 **Dish Name**\n\n⏱ **Time:** ...\n🔥 **Kcal:** ...\n\n🛒 **Ingredients:**\n..."
        )
    return prompt

def make_bonus_prompt(ingredients, lang='ru'):
    if lang == 'ru':
        return (
            f"У пользователя есть продукты: {ingredients}. "
            f"Предложи добавить ОДИН СОВЕРШЕННО НОВЫЙ ключевой ингредиент (например, мясо, курицу, томаты, грибы), "
            f"который КАРДИНАЛЬНО изменит блюдо. "
            f"СТРОГИЕ ЗАПРЕТЫ: "
            f"1) ЗАПРЕЩЕНО предлагать специи, соусы, масло, воду. "
            f"2) ЗАПРЕЩЕНО предлагать другие сорта того, что уже есть. "
            f"Ответь СТРОГО В ОДНУ СТРОКУ в формате: ИНГРЕДИЕНТ|НАЗВАНИЕ_БЛЮДА. "
            f"ЗАПРЕЩЕНО писать списки, нумерацию или лишние слова. Пример: Грибы|Жульен"
        )
    return (
        f"User has products: {ingredients}. "
        f"Suggest adding ONE COMPLETELY NEW key ingredient (e.g., meat, tomatoes, chicken, mushrooms) "
        f"that RADICALLY changes the dish. "
        f"STRICT BANS: "
        f"1) FORBIDDEN to suggest spices, sauces, oil, water. "
        f"2) FORBIDDEN to suggest variations of existing items. "
        f"Answer STRICTLY IN ONE LINE format: INGREDIENT|DISH_NAME. "
        f"Example: Mushrooms|Julienne"
    )

# ==========================================
# 🍳 БИЗНЕС-ЛОГИКА
# ==========================================

def ask_cooking_method(chat_id, user_input, is_retry=False):
    lang = get_lang(chat_id)
    wait_msg = bot.send_message(chat_id, get_msg(chat_id, 'analyzing_methods'))
    
    prompt = make_methods_prompt(user_input, lang)
    response = get_gigachat_response(prompt)
    bot.delete_message(chat_id, wait_msg.message_id)
    
    if response == "ОШИБКА_API":
        bot.send_message(chat_id, "❌ Произошла ошибка при обращении к ИИ. Попробуйте еще раз позже.")
        return

    methods = [m.strip() for m in response.split(',')]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for method in methods:
        markup.add(types.KeyboardButton(method))
    
    markup.add(types.KeyboardButton(get_msg(chat_id, 'btn_method_any')))
    markup.add(types.KeyboardButton(get_msg(chat_id, 'btn_keep')))
    
    user_state[chat_id] = 'WAIT_METHOD'
    bot.send_message(chat_id, get_msg(chat_id, 'choose_method'), reply_markup=markup, parse_mode='Markdown')

def suggest_bonus_recipe(chat_id, ingredients):
    lang = get_lang(chat_id)
    response = get_gigachat_response(make_bonus_prompt(ingredients, lang))
    
    if response == "ОШИБКА_API":
        return

    try:
        if "|" in response:
            extra_ing, dish_name = response.split("|", 1)
            extra_ing = extra_ing.strip(' 1234567890.-*')
            dish_name = dish_name.strip(' 1234567890.-*')
            user_bonus_ingredient[chat_id] = extra_ing
            
            text = get_msg(chat_id, 'bonus_found', ing=extra_ing, dish=dish_name)
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                get_msg(chat_id, 'btn_get_bonus', dish=dish_name[:20]), 
                callback_data=f"get_bonus:{dish_name[:20]}"
            )
            markup.add(btn)
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"Ошибка бонуса: {e}")

def send_recipe(chat_id, user_input, method, is_retry=False):
    lang = get_lang(chat_id)
    mode = get_mode(chat_id)
    basic = user_basic_ingredients.get(chat_id, MESSAGES[lang]['default_basic'])

    if mode == 'reverse':
        prompt = make_reverse_recipe_prompt(user_input, method, lang)
    elif mode == 'bonus':
        dish_name = user_target_dish.get(chat_id, "Блюдо")
        extra_ing = user_bonus_ingredient.get(chat_id, "")
        combined_ingredients = f"{user_input}, {extra_ing}" if extra_ing else user_input
        prompt = make_bonus_recipe_prompt(combined_ingredients, basic, dish_name, method, lang)
    else:
        prompt = make_recipe_prompt(user_input, basic, method, lang, is_retry)

    wait_msg = bot.send_message(chat_id, get_msg(chat_id, 'thinking'), reply_markup=types.ReplyKeyboardRemove())
    recipe_text = get_gigachat_response(prompt)

    bot.delete_message(chat_id, wait_msg.message_id)

    if recipe_text == "ОШИБКА_API":
        bot.send_message(chat_id, "❌ Произошла ошибка генерации рецепта. Попробуйте еще раз позже.", reply_markup=create_main_menu_keyboard(chat_id))
        user_state[chat_id] = 'MAIN_MENU'
        return

    try:
        dish_name_clean = recipe_text.split('\n')[0].replace('*', '').replace('🍽', '').strip()
    except:
        dish_name_clean = get_msg(chat_id, 'dish_fallback')

    ya_url = f"https://yandex.ru/images/search?text={dish_name_clean}"
    link_text = get_msg(chat_id, 'link_yandex')
    final_text = f"{recipe_text}\n\n[{link_text}]({ya_url})"

    inline_markup = types.InlineKeyboardMarkup()
    btn_regen = types.InlineKeyboardButton(get_msg(chat_id, 'btn_regen'), callback_data='regenerate')
    inline_markup.add(btn_regen)

    bot.send_message(chat_id, final_text, parse_mode='Markdown', reply_markup=inline_markup)
    
    user_state[chat_id] = 'MAIN_MENU'
    bot.send_message(chat_id, get_msg(chat_id, 'bon_appetit'), reply_markup=create_main_menu_keyboard(chat_id))
    
    if mode == 'normal':
        suggest_bonus_recipe(chat_id, user_input)

# ==========================================
# 🎮 ОБРАБОТЧИКИ (HANDLERS)
# ==========================================

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_state[message.chat.id] = 'WAIT_LANG'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇬🇧 English"))
    bot.send_message(message.chat.id, "🌍 Choose language / Выберите язык:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    if call.data.startswith("get_bonus:"):
        dish_name = call.data.split(":")[1]
        bot.answer_callback_query(call.id, "Окей, предлагаю способы...")
        user_mode[chat_id] = 'bonus'
        user_target_dish[chat_id] = dish_name
        ask_cooking_method(chat_id, dish_name, is_retry=True)
    elif call.data == 'regenerate':
        bot.answer_callback_query(call.id, get_msg(chat_id, 'searching'))
        ingredients = user_last_ingredients.get(chat_id)
        if not ingredients: return
        
        mode = get_mode(chat_id)
        if mode == 'bonus':
            ask_cooking_method(chat_id, user_target_dish[chat_id], is_retry=True)
        else:
            ask_cooking_method(chat_id, ingredients, is_retry=True)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    msg = message.text
    state = user_state.get(chat_id)
    lang = get_lang(chat_id)

    if state == 'WAIT_LANG':
        if msg == "🇷🇺 Русский":
            user_language[chat_id] = 'ru'
            user_state[chat_id] = 'MAIN_MENU'
            bot.send_message(chat_id, get_msg(chat_id, 'welcome_text'), parse_mode='Markdown')
            bot.send_message(chat_id, get_msg(chat_id, 'menu_text'), parse_mode='Markdown', reply_markup=create_main_menu_keyboard(chat_id))
        elif msg == "🇬🇧 English":
            user_language[chat_id] = 'en'
            user_state[chat_id] = 'MAIN_MENU'
            bot.send_message(chat_id, get_msg(chat_id, 'welcome_text'), parse_mode='Markdown')
            bot.send_message(chat_id, get_msg(chat_id, 'menu_text'), parse_mode='Markdown', reply_markup=create_main_menu_keyboard(chat_id))

    elif state == 'MAIN_MENU':
        if msg == get_msg(chat_id, 'btn_menu_ing'):
            user_mode[chat_id] = 'normal'
            user_state[chat_id] = 'WAIT_INPUT_INGREDIENTS'
            bot.send_message(chat_id, get_msg(chat_id, 'ask_ing'), parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
        elif msg == get_msg(chat_id, 'btn_menu_dish'):
            user_mode[chat_id] = 'reverse'
            user_state[chat_id] = 'WAIT_INPUT_DISH'
            bot.send_message(chat_id, get_msg(chat_id, 'ask_dish'), parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
        elif msg == get_msg(chat_id, 'btn_menu_basic'):
            user_state[chat_id] = 'WAIT_BASIC_ACTION'
            bot.send_message(chat_id, get_msg(chat_id, 'basic_info', basic=user_basic_ingredients.get(chat_id, MESSAGES[lang]['default_basic'])), reply_markup=create_basic_setup_keyboard(chat_id), parse_mode='Markdown')
        elif msg == get_msg(chat_id, 'btn_menu_lang'): start_handler(message)

    elif state == 'WAIT_BASIC_ACTION':
        if msg == get_msg(chat_id, 'btn_keep'):
            user_state[chat_id] = 'MAIN_MENU'
            bot.send_message(chat_id, get_msg(chat_id, 'menu_text'), reply_markup=create_main_menu_keyboard(chat_id))
        elif msg == get_msg(chat_id, 'btn_overwrite'):
            user_state[chat_id] = 'WAIT_BASIC_OVERWRITE'
            bot.send_message(chat_id, get_msg(chat_id, 'ask_overwrite'), parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
        elif msg == get_msg(chat_id, 'btn_add'):
            user_state[chat_id] = 'WAIT_BASIC_ADD'
            bot.send_message(chat_id, get_msg(chat_id, 'ask_add'), parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())

    elif state == 'WAIT_BASIC_OVERWRITE':
        check_msg = bot.send_message(chat_id, get_msg(chat_id, 'checking'))
        val_resp = get_gigachat_response(make_validation_prompt(msg, lang))
        bot.delete_message(chat_id, check_msg.message_id)
        
        if val_resp == "ОШИБКА_API":
            bot.send_message(chat_id, "❌ Проблема со связью с нейросетью. Попробуйте позже.")
            return 
            
        if "ОШИБКА" in val_resp.upper() or "ERROR" in val_resp.upper():
            bot.send_message(chat_id, get_msg(chat_id, 'not_basic_products'), parse_mode='Markdown')
            return 
        user_basic_ingredients[chat_id] = msg
        bot.send_message(chat_id, get_msg(chat_id, 'basic_updated', basic=msg), parse_mode='Markdown')
        user_state[chat_id] = 'WAIT_BASIC_ACTION'
        bot.send_message(chat_id, get_msg(chat_id, 'basic_info', basic=msg), parse_mode='Markdown', reply_markup=create_basic_setup_keyboard(chat_id))

    elif state == 'WAIT_BASIC_ADD':
        check_msg = bot.send_message(chat_id, get_msg(chat_id, 'checking'))
        val_resp = get_gigachat_response(make_validation_prompt(msg, lang))
        bot.delete_message(chat_id, check_msg.message_id)
        
        if val_resp == "ОШИБКА_API":
            bot.send_message(chat_id, "❌ Проблема со связью с нейросетью. Попробуйте позже.")
            return 
            
        if "ОШИБКА" in val_resp.upper() or "ERROR" in val_resp.upper():
            bot.send_message(chat_id, get_msg(chat_id, 'not_basic_products'), parse_mode='Markdown')
            return 
        current = user_basic_ingredients.get(chat_id, MESSAGES[lang]['default_basic'])
        new_list = f"{current}, {msg}"
        user_basic_ingredients[chat_id] = new_list
        bot.send_message(chat_id, get_msg(chat_id, 'basic_updated', basic=new_list), parse_mode='Markdown')
        user_state[chat_id] = 'WAIT_BASIC_ACTION'
        bot.send_message(chat_id, get_msg(chat_id, 'basic_info', basic=new_list), parse_mode='Markdown', reply_markup=create_basic_setup_keyboard(chat_id))

    elif state == 'WAIT_INPUT_INGREDIENTS':
        check_msg = bot.send_message(chat_id, get_msg(chat_id, 'checking'))
        val_resp = get_gigachat_response(make_validation_prompt(msg, lang))
        bot.delete_message(chat_id, check_msg.message_id)
        
        if val_resp == "ОШИБКА_API":
            bot.send_message(chat_id, "❌ Проблема со связью с нейросетью. Попробуйте позже.")
            return 
            
        if "ОШИБКА" in val_resp.upper() or "ERROR" in val_resp.upper():
            bot.send_message(chat_id, get_msg(chat_id, 'not_products'), parse_mode='Markdown')
            return 
        user_last_ingredients[chat_id] = msg
        ask_cooking_method(chat_id, msg)

    elif state == 'WAIT_INPUT_DISH':
        check_msg = bot.send_message(chat_id, get_msg(chat_id, 'checking'))
        val_resp = get_gigachat_response(make_dish_validation_prompt(msg, lang))
        bot.delete_message(chat_id, check_msg.message_id)
        
        if val_resp == "ОШИБКА_API":
            bot.send_message(chat_id, "❌ Проблема со связью с нейросетью. Попробуйте позже.")
            return 
            
        if "ОШИБКА" in val_resp.upper() or "ERROR" in val_resp.upper():
            bot.send_message(chat_id, get_msg(chat_id, 'not_dish'), parse_mode='Markdown')
            return
        user_last_ingredients[chat_id] = msg
        ask_cooking_method(chat_id, msg)

    elif state == 'WAIT_METHOD':
        if msg == get_msg(chat_id, 'btn_keep'):
            user_state[chat_id] = 'MAIN_MENU'
            bot.send_message(chat_id, get_msg(chat_id, 'menu_text'), reply_markup=create_main_menu_keyboard(chat_id))
        else:
            send_recipe(chat_id, user_last_ingredients.get(chat_id), msg)

if __name__ == '__main__':
    print("Бот на GigaChat запущен...")
    bot.polling(non_stop=True)