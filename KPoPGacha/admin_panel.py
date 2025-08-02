from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import ADMIN_IDS
from pb_client import PBClient

# Создаем экземпляр PBClient
pb = PBClient()

# Состояния для ConversationHandler
ADMIN_MENU = 0
ADD_STARS_MENU, ADD_STARS_AMOUNT, ADD_STARS_USER, GIVE_CARDS_MENU, GIVE_CARDS_USER, GIVE_CARDS_AMOUNT = range(1, 7)

async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню админ-панели"""
    user_id = update.effective_user.id
    print(f"DEBUG: [admin_start] Пользователь {user_id} пытается получить доступ к админ-панели")
    print(f"DEBUG: [admin_start] ADMIN_IDS: {ADMIN_IDS}")
    print(f"DEBUG: [admin_start] user_id in ADMIN_IDS: {user_id in ADMIN_IDS}")
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return ConversationHandler.END
    
    keyboard = [
        [InlineKeyboardButton("👥 Управление пользователями", callback_data="admin_users_menu")],
        [InlineKeyboardButton("🎴 Управление карточками", callback_data="admin_cards_menu")],
        [InlineKeyboardButton("💰 Экономика", callback_data="admin_economy_menu")],
        [InlineKeyboardButton("🎮 Игровые механики", callback_data="admin_game_menu")],
        [InlineKeyboardButton("📊 Аналитика и мониторинг", callback_data="admin_analytics_menu")],
        [InlineKeyboardButton("⚙️ Системные команды", callback_data="admin_system_menu")],
        [InlineKeyboardButton("🎉 Праздничные функции", callback_data="admin_events_menu")],
        [InlineKeyboardButton("🛡️ Модерация", callback_data="admin_moderation_menu")],
        [InlineKeyboardButton("📈 Статистика и отчеты", callback_data="admin_reports_menu")],
        [InlineKeyboardButton("❌ Отмена", callback_data="admin_cancel")]
    ]
    
    await update.message.reply_text(
        "🔧 <b>Админ-панель</b>\n\nВыберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
    return ADMIN_MENU

async def admin_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка callback'ов админ-меню"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "admin_users_menu":
        keyboard = [
            [InlineKeyboardButton("🚫 Заблокировать пользователя", callback_data="admin_ban_info")],
            [InlineKeyboardButton("✅ Разблокировать пользователя", callback_data="admin_unban_info")],
            [InlineKeyboardButton("🔄 Сбросить прогресс пользователя", callback_data="admin_reset_user_info")],
            [InlineKeyboardButton("📊 Установить уровень", callback_data="admin_set_level_info")],
            [InlineKeyboardButton("⭐ Установить опыт", callback_data="admin_set_exp_info")],
            [InlineKeyboardButton("👤 Информация о пользователе", callback_data="admin_user_info_info")],
            [InlineKeyboardButton("📜 История пользователя", callback_data="admin_user_history_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "👥 <b>Управление пользователями</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_cards_menu":
        keyboard = [
            [InlineKeyboardButton("➕ Добавить карточку пользователю", callback_data="admin_add_card_info")],
            [InlineKeyboardButton("➖ Удалить карточку у пользователя", callback_data="admin_remove_card_info")],
            [InlineKeyboardButton("🔄 Дублировать карточку", callback_data="admin_duplicate_card_info")],
            [InlineKeyboardButton("🎴 Выдать случайные карточки", callback_data="admin_give_cards")],
            [InlineKeyboardButton("📊 Статистика карточки", callback_data="admin_card_stats_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "🎴 <b>Управление карточками</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_economy_menu":
        keyboard = [
            [InlineKeyboardButton("⭐ Добавить всем звезд", callback_data="admin_add_stars_all")],
            [InlineKeyboardButton("👤 Добавить звезд пользователю", callback_data="admin_add_stars_user")],
            [InlineKeyboardButton("💰 Установить звезды пользователю", callback_data="admin_set_stars_info")],
            [InlineKeyboardButton("📈 Умножить звезды у всех", callback_data="admin_multiply_stars_info")],
            [InlineKeyboardButton("🔄 Сбросить ежедневные бонусы", callback_data="admin_daily_reset_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "💰 <b>Экономика</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_game_menu":
        keyboard = [
            [InlineKeyboardButton("🎯 Установить баннер пользователю", callback_data="admin_set_banner_info")],
            [InlineKeyboardButton("🔄 Сбросить баннеры у всех", callback_data="admin_reset_banners_info")],
            [InlineKeyboardButton("🏆 Выдать достижение", callback_data="admin_give_achievement_info")],
            [InlineKeyboardButton("🔄 Сбросить достижения", callback_data="admin_reset_achievements_info")],
            [InlineKeyboardButton("🎰 Установить pity", callback_data="admin_set_pity_info")],
            [InlineKeyboardButton("⭐ Выдать опыт пользователю", callback_data="admin_give_exp_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "🎮 <b>Игровые механики</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_analytics_menu":
        keyboard = [
            [InlineKeyboardButton("👥 Топ пользователей", callback_data="admin_top_users_info")],
            [InlineKeyboardButton("📊 Статистика карточки", callback_data="admin_card_stats_info")],
            [InlineKeyboardButton("📈 Лог активности", callback_data="admin_activity_log_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "📊 <b>Аналитика и мониторинг</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_system_menu":
        keyboard = [
            [InlineKeyboardButton("💾 Создать резервную копию", callback_data="admin_backup_info")],
            [InlineKeyboardButton("🔧 Режим обслуживания", callback_data="admin_maintenance_info")],
            [InlineKeyboardButton("📢 Отправить объявление", callback_data="admin_announce_info")],
            [InlineKeyboardButton("🔔 Тест уведомлений", callback_data="admin_test_notification_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "⚙️ <b>Системные команды</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_events_menu":
        keyboard = [
            [InlineKeyboardButton("🎉 Запустить событие", callback_data="admin_event_start_info")],
            [InlineKeyboardButton("🔚 Завершить событие", callback_data="admin_event_end_info")],
            [InlineKeyboardButton("🎁 Выдать награды события", callback_data="admin_give_event_rewards_info")],
            [InlineKeyboardButton("🎴 Установить баннер события", callback_data="admin_set_event_banner_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "🎉 <b>Праздничные функции</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_moderation_menu":
        keyboard = [
            [InlineKeyboardButton("⚠️ Предупреждение", callback_data="admin_warn_info")],
            [InlineKeyboardButton("🔇 Замутить пользователя", callback_data="admin_mute_info")],
            [InlineKeyboardButton("🔊 Размутить пользователя", callback_data="admin_unmute_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "🛡️ <b>Модерация</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_reports_menu":
        keyboard = [
            [InlineKeyboardButton("📊 Ежедневный отчет", callback_data="admin_daily_report_info")],
            [InlineKeyboardButton("📈 Еженедельный отчет", callback_data="admin_weekly_report_info")],
            [InlineKeyboardButton("💰 Статистика доходов", callback_data="admin_revenue_stats_info")],
            [InlineKeyboardButton("🔥 Популярные карточки", callback_data="admin_popular_cards_info")],
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            "📈 <b>Статистика и отчеты</b>\n\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    # Информационные callback'ы для команд
    elif query.data.endswith("_info"):
        command_name = query.data.replace("_info", "")
        info_text = get_command_info(command_name)
        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]
        ]
        await query.edit_message_text(
            f"ℹ️ <b>Информация о команде</b>\n\n{info_text}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU
    
    elif query.data == "admin_add_stars_all":
        await query.edit_message_text(
            "⭐ <b>Добавить всем звезд</b>\n\nИспользуйте команду:\n<code>/admin_stars [количество] [причина]</code>\n\nПример:\n<code>/admin_stars 500 Праздничный бонус</code>",
            parse_mode="HTML"
        )
        return await show_admin_back_menu(query)
    
    elif query.data == "admin_add_stars_user":
        await query.edit_message_text(
            "👤 <b>Добавить звезд пользователю</b>\n\nИспользуйте команду:\n<code>/admin_stars_user [ID] [количество]</code>\n\nПример:\n<code>/admin_stars_user 123456789 100</code>",
            parse_mode="HTML"
        )
        return await show_admin_back_menu(query)
    
    elif query.data == "admin_give_cards":
        await query.edit_message_text(
            "🎴 <b>Выдать карточки пользователю</b>\n\nИспользуйте команду:\n<code>/admin_give_cards [ID] [количество]</code>\n\nПример:\n<code>/admin_give_cards 123456789 10</code>",
            parse_mode="HTML"
        )
        return await show_admin_back_menu(query)
    
    elif query.data == "admin_cancel":
        await query.edit_message_text("❌ Операция отменена.")
        return ConversationHandler.END
    
    elif query.data == "admin_back":
        # Возвращаемся к главному меню админ-панели
        keyboard = [
            [InlineKeyboardButton("👥 Управление пользователями", callback_data="admin_users_menu")],
            [InlineKeyboardButton("🎴 Управление карточками", callback_data="admin_cards_menu")],
            [InlineKeyboardButton("💰 Экономика", callback_data="admin_economy_menu")],
            [InlineKeyboardButton("🎮 Игровые механики", callback_data="admin_game_menu")],
            [InlineKeyboardButton("📊 Аналитика и мониторинг", callback_data="admin_analytics_menu")],
            [InlineKeyboardButton("⚙️ Системные команды", callback_data="admin_system_menu")],
            [InlineKeyboardButton("🎉 Праздничные функции", callback_data="admin_events_menu")],
            [InlineKeyboardButton("🛡️ Модерация", callback_data="admin_moderation_menu")],
            [InlineKeyboardButton("📈 Статистика и отчеты", callback_data="admin_reports_menu")],
            [InlineKeyboardButton("❌ Отмена", callback_data="admin_cancel")]
        ]
        
        await query.edit_message_text(
            "🔧 <b>Админ-панель</b>\n\nВыберите категорию:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return ADMIN_MENU

async def admin_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена админ-операции"""
    await update.message.reply_text("❌ Операция отменена.")
    return ConversationHandler.END

async def show_admin_back_menu(query):
    """Показать кнопку "Назад" для админ-меню"""
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="admin_back")]]
    await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
    return ADMIN_MENU

# Вспомогательные функции
async def add_stars_to_all(amount):
    """Добавить звезды всем пользователям"""
    users = pb.get_all_users()
    for user in users:
        current_stars = user.get("stars", 0)
        new_stars = current_stars + amount
        pb.update_user_stars_and_pity(
            user["id"], 
            new_stars, 
            user.get("pity_legendary", 0), 
            user.get("pity_void", 0)
        )

async def add_stars_to_all_with_notification(amount, reason, update):
    """Добавить звезды всем пользователям и отправить уведомление"""
    users = pb.get_all_users()
    success_count = 0
    failed_count = 0
    
    # Сначала добавляем звезды всем
    for user in users:
        current_stars = user.get("stars", 0)
        new_stars = current_stars + amount
        pb.update_user_stars_and_pity(
            user["id"], 
            new_stars, 
            user.get("pity_legendary", 0), 
            user.get("pity_void", 0)
        )
    
    # Затем отправляем уведомления
    for user in users:
        telegram_id = user.get("telegram_id")
        if telegram_id:
            try:
                message_text = f"⭐ <b>Бонус!</b>\n\nВам добавлено <b>{amount} звезд</b>\n\nПричина: {reason}"
                await update.get_bot().send_message(
                    chat_id=telegram_id,
                    text=message_text,
                    parse_mode="HTML"
                )
                success_count += 1
            except Exception as e:
                print(f"DEBUG: [add_stars_to_all_with_notification] Ошибка отправки сообщения пользователю {telegram_id}: {e}")
                failed_count += 1
    
    print(f"DEBUG: [add_stars_to_all_with_notification] Успешно отправлено: {success_count}, Ошибок: {failed_count}")

async def add_stars_to_user(user_id, amount):
    """Добавить звезды конкретному пользователю"""
    pb_user = pb.get_user_by_telegram_id(user_id)
    if pb_user:
        current_stars = pb_user.get("stars", 0)
        new_stars = current_stars + amount
        pb.update_user_stars_and_pity(
            pb_user["id"], 
            new_stars, 
            pb_user.get("pity_legendary", 0), 
            pb_user.get("pity_void", 0)
        )

async def give_random_cards(user_id, amount):
    """Выдать случайные карточки пользователю"""
    pb_user = pb.get_user_by_telegram_id(user_id)
    if not pb_user:
        return
    
    # Получаем все карточки
    all_cards = pb.get_all_cards()
    if not all_cards:
        return
    
    # Выбираем случайные карточки
    import random
    selected_cards = random.sample(all_cards, min(amount, len(all_cards)))
    
    # Добавляем карточки пользователю
    for card in selected_cards:
        pb.add_card_to_user(pb_user["id"], card["id"])

async def reset_pity_all():
    """Сбросить pity для всех пользователей"""
    users = pb.get_all_users()
    for user in users:
        pb.update_user_stars_and_pity(
            user["id"], 
            user.get("stars", 0), 
            0,  # pity_legendary
            0   # pity_void
        )

async def get_admin_stats():
    """Получить статистику для админа"""
    users = pb.get_all_users()
    cards = pb.get_all_cards()
    
    total_users = len(users)
    total_cards = len(cards)
    total_stars = sum(user.get("stars", 0) for user in users)
    
    # Подсчет карточек по редкости
    rarity_stats = {}
    for card in cards:
        rarity = card.get("rarity", 1)
        rarity_stats[rarity] = rarity_stats.get(rarity, 0) + 1
    
    stats_text = f"""
👥 <b>Пользователей:</b> {total_users}
🎴 <b>Всего карточек:</b> {total_cards}
⭐ <b>Всего звезд:</b> {total_stars}

<b>Карточки по редкости:</b>
"""
    
    for rarity in sorted(rarity_stats.keys()):
        count = rarity_stats[rarity]
        stats_text += f"{rarity}★: {count}\n"
    
    return stats_text

# Создание ConversationHandler для админ-панели
def get_admin_conversation_handler():
    """Возвращает ConversationHandler для админ-панели"""
    return ConversationHandler(
        entry_points=[CommandHandler("admin", admin_start)],
        states={
            ADMIN_MENU: [
                CallbackQueryHandler(admin_menu_callback, pattern="^admin_")
            ]
        },
        fallbacks=[CommandHandler("admin", admin_start)],
        per_message=False
    )

# Функция для обработки админ-callback'ов вне ConversationHandler
async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка админ-callback'ов для прямых действий"""
    query = update.callback_query
    await query.answer()
    data = query.data
    
    print(f"DEBUG: [handle_admin_callback] Обрабатываю callback: {data}")
    
    # Проверяем права доступа
    user_id = query.from_user.id
    print(f"DEBUG: [handle_admin_callback] Пользователь {user_id} пытается получить доступ к админ-функциям")
    print(f"DEBUG: [handle_admin_callback] ADMIN_IDS: {ADMIN_IDS}")
    print(f"DEBUG: [handle_admin_callback] user_id in ADMIN_IDS: {user_id in ADMIN_IDS}")
    
    if user_id not in ADMIN_IDS:
        await query.edit_message_text("⛔ Доступ запрещен.")
        return
    
    # Обрабатываем только прямые админ-действия, не меню навигацию
    if data == "admin_add_stars_all":
        print(f"DEBUG: [handle_admin_callback] Обрабатываю admin_add_stars_all")
        await query.edit_message_text(
            "⭐ <b>Добавить всем звезд</b>\n\nИспользуйте команду:\n<code>/admin_stars [количество] [причина]</code>\n\nПример:\n<code>/admin_stars 500 Праздничный бонус</code>",
            parse_mode="HTML"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
        return
    
    elif data == "admin_add_stars_user":
        print(f"DEBUG: [handle_admin_callback] Обрабатываю admin_add_stars_user")
        await query.edit_message_text(
            "👤 <b>Добавить звезд пользователю</b>\n\nИспользуйте команду:\n<code>/admin_stars_user [ID] [количество]</code>\n\nПример:\n<code>/admin_stars_user 123456789 100</code>",
            parse_mode="HTML"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
        return
    
    elif data == "admin_give_cards":
        print(f"DEBUG: [handle_admin_callback] Обрабатываю admin_give_cards")
        await query.edit_message_text(
            "🎴 <b>Выдать карточки пользователю</b>\n\nИспользуйте команду:\n<code>/admin_give_cards [ID] [количество]</code>\n\nПример:\n<code>/admin_give_cards 123456789 10</code>",
            parse_mode="HTML"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
        return
    
    elif data == "admin_stats":
        print(f"DEBUG: [handle_admin_callback] Обрабатываю admin_stats")
        stats = await get_admin_stats()
        await query.edit_message_text(
            f"📊 <b>Статистика</b>\n\n{stats}",
            parse_mode="HTML"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
        return
    
    elif data == "admin_reset_pity":
        print(f"DEBUG: [handle_admin_callback] Обрабатываю admin_reset_pity")
        await reset_pity_all()
        await query.edit_message_text(
            "🔄 <b>Pity сброшен для всех пользователей</b>",
            parse_mode="HTML"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
        return
    
    elif data == "admin_cancel":
        print(f"DEBUG: [handle_admin_callback] Обрабатываю admin_cancel")
        await query.edit_message_text("❌ Операция отменена.")
        return
    
    # Если это не прямой админ-действие, пропускаем для обработки ConversationHandler
    print(f"DEBUG: [handle_admin_callback] Пропускаю callback для ConversationHandler: {data}")
    return False 

# Команды для админ-функций
async def admin_ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для блокировки пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Использование: /admin_ban [ID] [причина]")
        return
    
    try:
        target_id = int(context.args[0])
        reason = " ".join(context.args[1:])
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        # Добавляем поле banned в базу данных
        pb.ban_user(target_id, reason)
        await update.message.reply_text(f"🚫 Пользователь {pb_user.get('name', 'Неизвестно')} заблокирован!\n\nПричина: {reason}")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для разблокировки пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_unban [ID]")
        return
    
    try:
        target_id = int(context.args[0])
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        pb.unban_user(target_id)
        await update.message.reply_text(f"✅ Пользователь {pb_user.get('name', 'Неизвестно')} разблокирован!")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_reset_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для сброса прогресса пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_reset_user [ID]")
        return
    
    try:
        target_id = int(context.args[0])
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        pb.reset_user_progress(target_id)
        await update.message.reply_text(f"🔄 Прогресс пользователя {pb_user.get('name', 'Неизвестно')} сброшен!")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_set_level_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для установки уровня пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_set_level [ID] [уровень]")
        return
    
    try:
        target_id = int(context.args[0])
        level = int(context.args[1])
        
        if level < 1 or level > 100:
            await update.message.reply_text("❌ Уровень должен быть от 1 до 100!")
            return
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        pb.set_user_level(target_id, level)
        await update.message.reply_text(f"📈 Уровень пользователя {pb_user.get('name', 'Неизвестно')} установлен на {level}!")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_set_exp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для установки опыта пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_set_exp [ID] [опыт]")
        return
    
    try:
        target_id = int(context.args[0])
        exp = int(context.args[1])
        
        if exp < 0:
            await update.message.reply_text("❌ Опыт не может быть отрицательным!")
            return
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        pb.set_user_exp(target_id, exp)
        await update.message.reply_text(f"⭐ Опыт пользователя {pb_user.get('name', 'Неизвестно')} установлен на {exp}!")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_add_card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для добавления карточки пользователю"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_add_card [ID] [card_id]")
        return

    try:
        target_id = int(context.args[0])
        card_id = context.args[1]

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        card = pb.get_card_by_id(card_id)
        if not card:
            await update.message.reply_text("❌ Карточка не найдена!")
            return

        pb.add_card_to_user(pb_user["id"], card_id)
        await update.message.reply_text(f"✅ Карточка {card.get('name', 'Неизвестно')} добавлена пользователю {pb_user.get('name', 'Неизвестно')}!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_remove_card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для удаления карточки у пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_remove_card [ID] [card_id]")
        return

    try:
        target_id = int(context.args[0])
        card_id = context.args[1]

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        card = pb.get_card_by_id(card_id)
        if not card:
            await update.message.reply_text("❌ Карточка не найдена!")
            return

        pb.remove_card_from_user(pb_user["id"], card_id)
        await update.message.reply_text(f"🗑️ Карточка {card.get('name', 'Неизвестно')} удалена у пользователя {pb_user.get('name', 'Неизвестно')}!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_duplicate_card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для дублирования карточки у пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 3:
        await update.message.reply_text("❌ Использование: /admin_duplicate_card [ID] [card_id] [количество]")
        return

    try:
        target_id = int(context.args[0])
        card_id = context.args[1]
        count = int(context.args[2])

        if count < 1 or count > 100:
            await update.message.reply_text("❌ Количество должно быть от 1 до 100!")
            return

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        card = pb.get_card_by_id(card_id)
        if not card:
            await update.message.reply_text("❌ Карточка не найдена!")
            return

        pb.duplicate_card_for_user(pb_user["id"], card_id, count)
        await update.message.reply_text(f"📋 Добавлено {count} копий карточки {card.get('name', 'Неизвестно')} пользователю {pb_user.get('name', 'Неизвестно')}!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_set_pity_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для установки pity пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 3:
        await update.message.reply_text("❌ Использование: /admin_set_pity [ID] [legendary] [void]")
        return

    try:
        target_id = int(context.args[0])
        legendary = int(context.args[1])
        void = int(context.args[2])

        if legendary < 0 or void < 0:
            await update.message.reply_text("❌ Pity не может быть отрицательным!")
            return

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        pb.set_user_pity(target_id, legendary, void)
        await update.message.reply_text(f"🎯 Pity пользователя {pb_user.get('name', 'Неизвестно')} установлен: Legendary {legendary}, Void {void}!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_multiply_stars_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для умножения звезд у всех пользователей"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_multiply_stars [множитель]")
        return

    try:
        multiplier = float(context.args[0])

        if multiplier <= 0:
            await update.message.reply_text("❌ Множитель должен быть больше 0!")
            return

        users = pb.get_all_users()
        updated_count = 0

        for user in users:
            current_stars = user.get("stars", 0)
            new_stars = int(current_stars * multiplier)
            pb.update_user_stars_and_pity(
                user["id"],
                new_stars,
                user.get("pity_legendary", 0),
                user.get("pity_void", 0)
            )
            updated_count += 1

        await update.message.reply_text(f"💰 Звезды всех пользователей умножены на {multiplier}!\n\nОбновлено пользователей: {updated_count}")

    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")

async def admin_daily_reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для сброса ежедневных бонусов у всех пользователей"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    users = pb.get_all_users()
    reset_count = 0

    for user in users:
        pb.reset_daily_bonus(user["id"])
        reset_count += 1

    await update.message.reply_text(f"🔄 Ежедневные бонусы сброшены у всех пользователей!\n\nСброшено пользователей: {reset_count}")

async def admin_give_exp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для выдачи опыта пользователю"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_give_exp [ID] [количество]")
        return

    try:
        target_id = int(context.args[0])
        exp_amount = int(context.args[1])

        if exp_amount < 0:
            await update.message.reply_text("❌ Количество опыта не может быть отрицательным!")
            return

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        current_exp = pb_user.get("exp", 0)
        new_exp = current_exp + exp_amount
        pb.set_user_exp(target_id, new_exp)
        
        await update.message.reply_text(f"⭐ Пользователю {pb_user.get('name', 'Неизвестно')} добавлено {exp_amount} опыта!\n\nТекущий опыт: {new_exp}")

    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_set_banner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для установки баннера пользователю"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 3:
        await update.message.reply_text("❌ Использование: /admin_set_banner [ID] [группа] [альбом]")
        return

    try:
        target_id = int(context.args[0])
        group = context.args[1]
        album = context.args[2]

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        pb.set_user_banner(target_id, group, album)
        await update.message.reply_text(f"🎯 Баннер пользователя {pb_user.get('name', 'Неизвестно')} установлен: {group} — {album}!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_reset_banners_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для сброса баннеров у всех пользователей"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    users = pb.get_all_users()
    reset_count = 0

    for user in users:
        pb.reset_user_banner(user["id"])
        reset_count += 1

    await update.message.reply_text(f"🔄 Баннеры сброшены у всех пользователей!\n\nСброшено пользователей: {reset_count}")

async def admin_give_achievement_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для выдачи достижения пользователю"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 4:
        await update.message.reply_text("❌ Использование: /admin_give_achievement [ID] [группа] [альбом] [уровень]")
        return

    try:
        target_id = int(context.args[0])
        group = context.args[1]
        album = context.args[2]
        level = int(context.args[3])

        if level not in [25, 50, 75, 100]:
            await update.message.reply_text("❌ Уровень достижения должен быть 25, 50, 75 или 100!")
            return

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        pb.give_achievement(pb_user["id"], group, album, level)
        await update.message.reply_text(f"🏆 Пользователю {pb_user.get('name', 'Неизвестно')} выдано достижение: {group} — {album} ({level}%)!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректные данные!")

async def admin_reset_achievements_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для сброса достижений пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_reset_achievements [ID]")
        return

    try:
        target_id = int(context.args[0])

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        pb.reset_user_achievements(pb_user["id"])
        await update.message.reply_text(f"🔄 Достижения пользователя {pb_user.get('name', 'Неизвестно')} сброшены!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_user_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения информации о пользователе"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_user_info [ID]")
        return

    try:
        target_id = int(context.args[0])

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        # Получаем дополнительную информацию
        inventory = pb.get_user_inventory(pb_user["id"])
        total_cards = sum(card.get("count", 1) for card in inventory)
        unique_cards = len(inventory)
        
        rank = pb.get_rank(pb_user.get('level', 1))
        group, album = pb.get_active_banner(pb_user)
        banner_str = f"{group} — {album}" if group and album else "Общий (все карты)"

        info_text = (
            f"👤 <b>Информация о пользователе:</b>\n\n"
            f"<b>ID:</b> {target_id}\n"
            f"<b>Имя:</b> {pb_user.get('name', 'Неизвестно')}\n"
            f"<b>Уровень:</b> {pb_user.get('level', 1)} ({rank})\n"
            f"<b>Опыт:</b> {pb_user.get('exp', 0)} / {pb.exp_to_next_level(pb_user.get('level', 1))}\n"
            f"<b>⭐ Звёзды:</b> {pb_user.get('stars', 0)}\n"
            f"<b>🎯 Pity Legendary:</b> {pb_user.get('pity_legendary', 0)} / 80\n"
            f"<b>🕳️ Pity Void:</b> {pb_user.get('pity_void', 0)} / 165\n"
            f"<b>📊 Карточек:</b> {total_cards} (уникальных: {unique_cards})\n"
            f"<b>🎯 Баннер:</b> {banner_str}\n"
            f"<b>🚫 Заблокирован:</b> {'Да' if pb_user.get('banned', False) else 'Нет'}"
        )

        if pb_user.get('banned', False):
            info_text += f"\n<b>Причина блокировки:</b> {pb_user.get('ban_reason', 'Не указана')}"

        await update.message.reply_text(info_text, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_top_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения топ пользователей"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        limit = 10
        if context.args and len(context.args) == 1:
            limit = int(context.args[0])
            if limit < 1 or limit > 50:
                await update.message.reply_text("❌ Количество должно быть от 1 до 50!")
                return

        users = pb.get_all_users()
        
        # Сортируем по уровню и опыту
        sorted_users = sorted(users, key=lambda x: (x.get('level', 1), x.get('exp', 0)), reverse=True)
        top_users = sorted_users[:limit]

        text = f"🏆 <b>Топ {len(top_users)} пользователей:</b>\n\n"
        
        for i, user in enumerate(top_users, 1):
            rank = pb.get_rank(user.get('level', 1))
            text += f"{i}. <b>{user.get('name', 'Неизвестно')}</b>\n"
            text += f"   Уровень: {user.get('level', 1)} ({rank})\n"
            text += f"   Опыт: {user.get('exp', 0)}\n"
            text += f"   ⭐ Звёзды: {user.get('stars', 0)}\n\n"

        await update.message.reply_text(text, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")

async def admin_card_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения статистики карточки"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_card_stats [card_id]")
        return

    try:
        card_id = context.args[0]

        card = pb.get_card_by_id(card_id)
        if not card:
            await update.message.reply_text("❌ Карточка не найдена!")
            return

        # Получаем статистику владения
        ownership_stats = pb.get_card_ownership_stats(card_id)
        total_owners = ownership_stats.get('total_owners', 0)
        total_copies = ownership_stats.get('total_copies', 0)

        stats_text = (
            f"📊 <b>Статистика карточки:</b>\n\n"
            f"<b>ID:</b> {card_id}\n"
            f"<b>Название:</b> {card.get('name', 'Неизвестно')}\n"
            f"<b>Группа:</b> {card.get('group', 'Неизвестно')}\n"
            f"<b>Альбом:</b> {card.get('album', 'Неизвестно')}\n"
            f"<b>Редкость:</b> {card.get('rarity', 0)}★\n"
            f"<b>Владельцев:</b> {total_owners}\n"
            f"<b>Всего копий:</b> {total_copies}\n"
            f"<b>Среднее на владельца:</b> {total_copies/total_owners if total_owners > 0 else 0:.1f}"
        )

        await update.message.reply_text(stats_text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении статистики: {str(e)}")

async def admin_activity_log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения лога активности"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        days = 7
        if context.args and len(context.args) == 1:
            days = int(context.args[0])
            if days < 1 or days > 30:
                await update.message.reply_text("❌ Количество дней должно быть от 1 до 30!")
                return

        # Получаем статистику активности
        activity_stats = pb.get_activity_stats(days)
        
        text = f"📈 <b>Статистика активности за {days} дней:</b>\n\n"
        text += f"<b>Новых пользователей:</b> {activity_stats.get('new_users', 0)}\n"
        text += f"<b>Активных пользователей:</b> {activity_stats.get('active_users', 0)}\n"
        text += f"<b>Всего попыток гачи:</b> {activity_stats.get('total_pulls', 0)}\n"
        text += f"<b>Среднее попыток на пользователя:</b> {activity_stats.get('avg_pulls_per_user', 0):.1f}\n"
        text += f"<b>Попыток сегодня:</b> {activity_stats.get('pulls_today', 0)}"

        await update.message.reply_text(text, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")

async def admin_backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для создания резервной копии"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        # Создаем резервную копию
        backup_data = pb.create_backup()
        
        text = "💾 <b>Резервная копия создана!</b>\n\n"
        text += f"<b>Пользователей:</b> {backup_data.get('users_count', 0)}\n"
        text += f"<b>Карточек:</b> {backup_data.get('cards_count', 0)}\n"
        text += f"<b>Попыток гачи:</b> {backup_data.get('pulls_count', 0)}\n"
        text += f"<b>Аукционов:</b> {backup_data.get('auctions_count', 0)}\n"
        text += f"<b>Достижений:</b> {backup_data.get('achievements_count', 0)}\n"
        text += f"<b>Время создания:</b> {backup_data.get('created_at', 'Неизвестно')}"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при создании резервной копии: {str(e)}")

async def admin_maintenance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для управления режимом обслуживания"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_maintenance [on/off]")
        return

    try:
        mode = context.args[0].lower()
        
        if mode not in ["on", "off"]:
            await update.message.reply_text("❌ Режим должен быть 'on' или 'off'!")
            return

        pb.set_maintenance_mode(mode == "on")
        
        if mode == "on":
            await update.message.reply_text("🔧 <b>Режим обслуживания включен!</b>\n\nБот временно недоступен для пользователей.")
        else:
            await update.message.reply_text("✅ <b>Режим обслуживания выключен!</b>\n\nБот снова доступен для пользователей.")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при изменении режима обслуживания: {str(e)}")

async def admin_announce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для отправки объявления всем пользователям"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) < 1:
        await update.message.reply_text("❌ Использование: /admin_announce [сообщение]")
        return

    try:
        message = " ".join(context.args)
        
        # Отправляем объявление всем пользователям
        users = pb.get_all_users()
        success_count = 0
        failed_count = 0

        for user in users:
            telegram_id = user.get("telegram_id")
            if telegram_id:
                try:
                    announce_text = f"📢 <b>Объявление от администрации:</b>\n\n{message}"
                    await update.get_bot().send_message(
                        chat_id=telegram_id,
                        text=announce_text,
                        parse_mode="HTML"
                    )
                    success_count += 1
                except Exception as e:
                    print(f"DEBUG: [admin_announce] Ошибка отправки сообщения пользователю {telegram_id}: {e}")
                    failed_count += 1

        await update.message.reply_text(
            f"📢 <b>Объявление отправлено!</b>\n\n"
            f"Успешно отправлено: {success_count}\n"
            f"Ошибок: {failed_count}",
            parse_mode="HTML"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при отправке объявления: {str(e)}")

async def admin_test_notification_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для тестирования уведомлений"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        # Отправляем тестовое уведомление только админу
        test_message = (
            "🧪 <b>Тестовое уведомление</b>\n\n"
            "Это тестовое сообщение для проверки работы системы уведомлений.\n"
            "Если вы получили это сообщение, значит система работает корректно!"
        )
        
        await update.message.reply_text(test_message, parse_mode="HTML")
        await update.message.reply_text("✅ Тестовое уведомление отправлено успешно!")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при отправке тестового уведомления: {str(e)}")

async def admin_event_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для запуска праздничного события"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_event_start [название] [длительность_дней]")
        return

    try:
        event_name = context.args[0]
        duration_days = int(context.args[1])

        if duration_days < 1 or duration_days > 30:
            await update.message.reply_text("❌ Длительность должна быть от 1 до 30 дней!")
            return

        # Запускаем событие
        event_data = pb.start_event(event_name, duration_days)
        
        text = f"🎉 <b>Праздничное событие запущено!</b>\n\n"
        text += f"<b>Название:</b> {event_name}\n"
        text += f"<b>Длительность:</b> {duration_days} дней\n"
        text += f"<b>Дата окончания:</b> {event_data.get('end_date', 'Неизвестно')}\n"
        text += f"<b>ID события:</b> {event_data.get('id', 'Неизвестно')}"

        await update.message.reply_text(text, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("❌ Введите корректную длительность!")

async def admin_event_end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для завершения праздничного события"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        # Завершаем активное событие
        event_data = pb.end_active_event()
        
        if event_data:
            text = f"🏁 <b>Праздничное событие завершено!</b>\n\n"
            text += f"<b>Название:</b> {event_data.get('name', 'Неизвестно')}\n"
            text += f"<b>Участников:</b> {event_data.get('participants_count', 0)}\n"
            text += f"<b>Время завершения:</b> {event_data.get('ended_at', 'Неизвестно')}"
        else:
            text = "❌ Активное событие не найдено!"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при завершении события: {str(e)}")

async def admin_give_event_rewards_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для выдачи наград участникам события"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_give_event_rewards [событие]")
        return

    try:
        event_name = context.args[0]
        
        # Выдаем награды участникам события
        rewards_data = pb.give_event_rewards(event_name)
        
        text = f"🎁 <b>Награды события выданы!</b>\n\n"
        text += f"<b>Событие:</b> {event_name}\n"
        text += f"<b>Участников:</b> {rewards_data.get('participants_count', 0)}\n"
        text += f"<b>Выдано наград:</b> {rewards_data.get('rewards_given', 0)}\n"
        text += f"<b>Звезд выдано:</b> {rewards_data.get('stars_given', 0)}"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при выдаче наград: {str(e)}")

async def admin_set_event_banner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для установки баннера события"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_set_event_banner [группа] [альбом]")
        return

    try:
        group = context.args[0]
        album = context.args[1]

        # Устанавливаем баннер события
        banner_data = pb.set_event_banner(group, album)
        
        text = f"🎯 <b>Баннер события установлен!</b>\n\n"
        text += f"<b>Группа:</b> {group}\n"
        text += f"<b>Альбом:</b> {album}\n"
        text += f"<b>Карточек в баннере:</b> {banner_data.get('cards_count', 0)}"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при установке баннера события: {str(e)}")

async def admin_warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для предупреждения пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Использование: /admin_warn [ID] [причина]")
        return

    try:
        target_id = int(context.args[0])
        reason = " ".join(context.args[1:])

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        # Добавляем предупреждение
        pb.add_warning(target_id, reason)
        
        # Отправляем уведомление пользователю
        try:
            warn_message = f"⚠️ <b>Предупреждение от администрации</b>\n\nПричина: {reason}\n\nПожалуйста, соблюдайте правила!"
            await update.get_bot().send_message(
                chat_id=target_id,
                text=warn_message,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"DEBUG: [admin_warn] Ошибка отправки предупреждения пользователю {target_id}: {e}")

        await update.message.reply_text(f"⚠️ Пользователю {pb_user.get('name', 'Неизвестно')} выдано предупреждение!\n\nПричина: {reason}")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для мута пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_mute [ID] [часы]")
        return

    try:
        target_id = int(context.args[0])
        hours = int(context.args[1])

        if hours < 1 or hours > 168:  # Максимум 7 дней
            await update.message.reply_text("❌ Количество часов должно быть от 1 до 168!")
            return

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        # Мутим пользователя
        pb.mute_user(target_id, hours)
        
        # Отправляем уведомление пользователю
        try:
            mute_message = f"🔇 <b>Вы были замучены администрацией</b>\n\nДлительность: {hours} часов\n\nПо истечении времени мут будет снят автоматически."
            await update.get_bot().send_message(
                chat_id=target_id,
                text=mute_message,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"DEBUG: [admin_mute] Ошибка отправки уведомления о муте пользователю {target_id}: {e}")

        await update.message.reply_text(f"🔇 Пользователь {pb_user.get('name', 'Неизвестно')} замучен на {hours} часов!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для размута пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_unmute [ID]")
        return

    try:
        target_id = int(context.args[0])

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        # Размучиваем пользователя
        pb.unmute_user(target_id)
        
        # Отправляем уведомление пользователю
        try:
            unmute_message = f"🔊 <b>Ваш мут был снят администрацией</b>\n\nТеперь вы снова можете использовать бота!"
            await update.get_bot().send_message(
                chat_id=target_id,
                text=unmute_message,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"DEBUG: [admin_unmute] Ошибка отправки уведомления о размуте пользователю {target_id}: {e}")

        await update.message.reply_text(f"🔊 Мут пользователя {pb_user.get('name', 'Неизвестно')} снят!")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_user_history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения истории пользователя"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Использование: /admin_user_history [ID]")
        return

    try:
        target_id = int(context.args[0])

        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return

        # Получаем историю пользователя
        history = pb.get_user_moderation_history(target_id)
        
        text = f"📋 <b>История пользователя {pb_user.get('name', 'Неизвестно')}:</b>\n\n"
        
        if not history:
            text += "История пуста."
        else:
            for i, record in enumerate(history, 1):
                action_type = record.get('type', 'Неизвестно')
                reason = record.get('reason', 'Не указана')
                created_at = record.get('created_at', 'Неизвестно')
                
                text += f"{i}. <b>{action_type}</b>\n"
                text += f"   Причина: {reason}\n"
                text += f"   Дата: {created_at}\n\n"

        await update.message.reply_text(text, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID!")

async def admin_daily_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения ежедневного отчета"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        # Получаем ежедневный отчет
        report = pb.get_daily_report()
        
        text = "📊 <b>Ежедневный отчет:</b>\n\n"
        text += f"<b>Новых пользователей:</b> {report.get('new_users', 0)}\n"
        text += f"<b>Активных пользователей:</b> {report.get('active_users', 0)}\n"
        text += f"<b>Всего попыток гачи:</b> {report.get('total_pulls', 0)}\n"
        text += f"<b>Попыток /pull:</b> {report.get('single_pulls', 0)}\n"
        text += f"<b>Попыток /pull10:</b> {report.get('ten_pulls', 0)}\n"
        text += f"<b>Выдано звезд:</b> {report.get('stars_given', 0)}\n"
        text += f"<b>Получено звезд:</b> {report.get('stars_earned', 0)}\n"
        text += f"<b>Создано аукционов:</b> {report.get('auctions_created', 0)}\n"
        text += f"<b>Завершено аукционов:</b> {report.get('auctions_completed', 0)}\n"
        text += f"<b>Активировано промокодов:</b> {report.get('promos_used', 0)}"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении отчета: {str(e)}")

async def admin_weekly_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения еженедельного отчета"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        # Получаем еженедельный отчет
        report = pb.get_weekly_report()
        
        text = "📈 <b>Еженедельный отчет:</b>\n\n"
        text += f"<b>Новых пользователей:</b> {report.get('new_users', 0)}\n"
        text += f"<b>Активных пользователей:</b> {report.get('active_users', 0)}\n"
        text += f"<b>Всего попыток гачи:</b> {report.get('total_pulls', 0)}\n"
        text += f"<b>Среднее попыток на пользователя:</b> {report.get('avg_pulls_per_user', 0):.1f}\n"
        text += f"<b>Выдано звезд:</b> {report.get('stars_given', 0)}\n"
        text += f"<b>Получено звезд:</b> {report.get('stars_earned', 0)}\n"
        text += f"<b>Создано аукционов:</b> {report.get('auctions_created', 0)}\n"
        text += f"<b>Завершено аукционов:</b> {report.get('auctions_completed', 0)}\n"
        text += f"<b>Активировано промокодов:</b> {report.get('promos_used', 0)}\n"
        text += f"<b>Выдано достижений:</b> {report.get('achievements_given', 0)}"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении отчета: {str(e)}")

async def admin_revenue_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения статистики доходов"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        # Получаем статистику доходов
        stats = pb.get_revenue_stats()
        
        text = "💰 <b>Статистика доходов:</b>\n\n"
        text += f"<b>Всего звезд в системе:</b> {stats.get('total_stars', 0)}\n"
        text += f"<b>Среднее звезд на пользователя:</b> {stats.get('avg_stars_per_user', 0):.1f}\n"
        text += f"<b>Максимум звезд у пользователя:</b> {stats.get('max_stars', 0)}\n"
        text += f"<b>Пользователей с 0 звезд:</b> {stats.get('users_with_zero_stars', 0)}\n"
        text += f"<b>Пользователей с 100+ звезд:</b> {stats.get('users_with_100_plus_stars', 0)}\n"
        text += f"<b>Пользователей с 1000+ звезд:</b> {stats.get('users_with_1000_plus_stars', 0)}"

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении статистики: {str(e)}")

async def admin_popular_cards_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения популярных карточек"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return

    try:
        limit = 10
        if context.args and len(context.args) == 1:
            limit = int(context.args[0])
            if limit < 1 or limit > 50:
                await update.message.reply_text("❌ Количество должно быть от 1 до 50!")
                return

        # Получаем популярные карточки
        popular_cards = pb.get_popular_cards(limit)
        
        text = f"🔥 <b>Топ {len(popular_cards)} популярных карточек:</b>\n\n"
        
        for i, card in enumerate(popular_cards, 1):
            text += f"{i}. <b>{card.get('name', 'Неизвестно')}</b>\n"
            text += f"   {card.get('group', 'Неизвестно')} — {card.get('album', 'Неизвестно')}\n"
            text += f"   Редкость: {card.get('rarity', 0)}★\n"
            text += f"   Владельцев: {card.get('owners_count', 0)}\n"
            text += f"   Всего копий: {card.get('total_copies', 0)}\n\n"

        await update.message.reply_text(text, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении статистики: {str(e)}")

async def admin_stars_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для добавления звезд всем пользователям"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text("❌ Использование: /admin_stars [количество] [причина]")
        return
    
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("❌ Количество должно быть положительным!")
            return
        
        # Получаем причину из оставшихся аргументов
        reason = " ".join(context.args[1:]) if len(context.args) > 1 else "Бонус от администрации"
        
        await add_stars_to_all_with_notification(amount, reason, update)
        await update.message.reply_text(f"✅ Добавлено {amount} звезд всем пользователям!\n\nПричина: {reason}")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")

async def admin_stars_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для добавления звезд конкретному пользователю"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_stars_user [ID] [количество]")
        return
    
    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
        
        if amount <= 0:
            await update.message.reply_text("❌ Количество должно быть положительным!")
            return
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        await add_stars_to_user(target_id, amount)
        await update.message.reply_text(f"✅ Добавлено {amount} звезд пользователю {pb_user.get('name', 'Неизвестно')}!")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!")

async def admin_give_cards_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для выдачи карточек пользователю"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return
    
    if not context.args or len(context.args) != 2:
        await update.message.reply_text("❌ Использование: /admin_give_cards [ID] [количество]")
        return
    
    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
        
        if amount <= 0 or amount > 100:
            await update.message.reply_text("❌ Количество должно быть от 1 до 100!")
            return
        
        pb_user = pb.get_user_by_telegram_id(target_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return
        
        await give_random_cards(target_id, amount)
        await update.message.reply_text(f"✅ Выдано {amount} случайных карточек пользователю {pb_user.get('name', 'Неизвестно')}!")
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректные числа!") 

def get_command_info(command_name):
    """Возвращает информацию о команде"""
    command_info = {
        "admin_ban": "🚫 <b>Заблокировать пользователя</b>\n\nИспользуйте: <code>/admin_ban [ID] [причина]</code>\n\nПример: <code>/admin_ban 123456789 Спам</code>\n\nЗаблокирует пользователя с указанным Telegram ID.",
        
        "admin_unban": "✅ <b>Разблокировать пользователя</b>\n\nИспользуйте: <code>/admin_unban [ID]</code>\n\nПример: <code>/admin_unban 123456789</code>\n\nРазблокирует пользователя с указанным Telegram ID.",
        
        "admin_reset_user": "🔄 <b>Сбросить прогресс пользователя</b>\n\nИспользуйте: <code>/admin_reset_user [ID]</code>\n\nПример: <code>/admin_reset_user 123456789</code>\n\nСбросит весь прогресс пользователя (карточки, звезды, уровень).",
        
        "admin_set_level": "📊 <b>Установить уровень</b>\n\nИспользуйте: <code>/admin_set_level [ID] [уровень]</code>\n\nПример: <code>/admin_set_level 123456789 50</code>\n\nУстановит указанный уровень пользователю.",
        
        "admin_set_exp": "⭐ <b>Установить опыт</b>\n\nИспользуйте: <code>/admin_set_exp [ID] [опыт]</code>\n\nПример: <code>/admin_set_exp 123456789 10000</code>\n\nУстановит указанное количество опыта пользователю.",
        
        "admin_user_info": "👤 <b>Информация о пользователе</b>\n\nИспользуйте: <code>/admin_user_info [ID]</code>\n\nПример: <code>/admin_user_info 123456789</code>\n\nПокажет подробную информацию о пользователе.",
        
        "admin_user_history": "📜 <b>История пользователя</b>\n\nИспользуйте: <code>/admin_user_history [ID]</code>\n\nПример: <code>/admin_user_history 123456789</code>\n\nПокажет историю действий пользователя.",
        
        "admin_add_card": "➕ <b>Добавить карточку пользователю</b>\n\nИспользуйте: <code>/admin_add_card [ID] [card_id]</code>\n\nПример: <code>/admin_add_card 123456789 card_123</code>\n\nДобавит указанную карточку пользователю.",
        
        "admin_remove_card": "➖ <b>Удалить карточку у пользователя</b>\n\nИспользуйте: <code>/admin_remove_card [ID] [card_id]</code>\n\nПример: <code>/admin_remove_card 123456789 card_123</code>\n\nУдалит указанную карточку у пользователя.",
        
        "admin_duplicate_card": "🔄 <b>Дублировать карточку</b>\n\nИспользуйте: <code>/admin_duplicate_card [ID] [card_id] [количество]</code>\n\nПример: <code>/admin_duplicate_card 123456789 card_123 5</code>\n\nДобавит указанное количество копий карточки пользователю.",
        
        "admin_card_stats": "📊 <b>Статистика карточки</b>\n\nИспользуйте: <code>/admin_card_stats [card_id]</code>\n\nПример: <code>/admin_card_stats card_123</code>\n\nПокажет статистику владения карточкой.",
        
        "admin_set_stars": "💰 <b>Установить звезды пользователю</b>\n\nИспользуйте: <code>/admin_set_stars [ID] [количество]</code>\n\nПример: <code>/admin_set_stars 123456789 1000</code>\n\nУстановит указанное количество звезд пользователю.",
        
        "admin_multiply_stars": "📈 <b>Умножить звезды у всех</b>\n\nИспользуйте: <code>/admin_multiply_stars [множитель]</code>\n\nПример: <code>/admin_multiply_stars 2</code>\n\nУмножит звезды у всех пользователей на указанный множитель.",
        
        "admin_daily_reset": "🔄 <b>Сбросить ежедневные бонусы</b>\n\nИспользуйте: <code>/admin_daily_reset</code>\n\nСбросит ежедневные бонусы у всех пользователей.",
        
        "admin_set_banner": "🎯 <b>Установить баннер пользователю</b>\n\nИспользуйте: <code>/admin_set_banner [ID] [группа] [альбом]</code>\n\nПример: <code>/admin_set_banner 123456789 BLACKPINK BORN PINK</code>\n\nУстановит указанный баннер пользователю.",
        
        "admin_reset_banners": "🔄 <b>Сбросить баннеры у всех</b>\n\nИспользуйте: <code>/admin_reset_banners</code>\n\nСбросит баннеры у всех пользователей.",
        
        "admin_give_achievement": "🏆 <b>Выдать достижение</b>\n\nИспользуйте: <code>/admin_give_achievement [ID] [группа] [альбом] [уровень]</code>\n\nПример: <code>/admin_give_achievement 123456789 BLACKPINK BORN PINK 100</code>\n\nВыдаст достижение пользователю.",
        
        "admin_reset_achievements": "🔄 <b>Сбросить достижения</b>\n\nИспользуйте: <code>/admin_reset_achievements [ID]</code>\n\nПример: <code>/admin_reset_achievements 123456789</code>\n\nСбросит все достижения пользователя.",
        
        "admin_set_pity": "🎰 <b>Установить pity</b>\n\nИспользуйте: <code>/admin_set_pity [ID] [legendary] [void]</code>\n\nПример: <code>/admin_set_pity 123456789 50 30</code>\n\nУстановит указанные значения pity пользователю.",
        
        "admin_give_exp": "⭐ <b>Выдать опыт пользователю</b>\n\nИспользуйте: <code>/admin_give_exp [ID] [количество]</code>\n\nПример: <code>/admin_give_exp 123456789 5000</code>\n\nДобавит указанное количество опыта пользователю.",
        
        "admin_top_users": "👥 <b>Топ пользователей</b>\n\nИспользуйте: <code>/admin_top_users [количество]</code>\n\nПример: <code>/admin_top_users 10</code>\n\nПокажет топ пользователей по уровню.",
        
        "admin_activity_log": "📈 <b>Лог активности</b>\n\nИспользуйте: <code>/admin_activity_log [дни]</code>\n\nПример: <code>/admin_activity_log 7</code>\n\nПокажет активность за указанное количество дней.",
        
        "admin_backup": "💾 <b>Создать резервную копию</b>\n\nИспользуйте: <code>/admin_backup</code>\n\nСоздаст резервную копию базы данных.",
        
        "admin_maintenance": "🔧 <b>Режим обслуживания</b>\n\nИспользуйте: <code>/admin_maintenance [on/off]</code>\n\nПример: <code>/admin_maintenance on</code>\n\nВключит/выключит режим обслуживания.",
        
        "admin_announce": "📢 <b>Отправить объявление</b>\n\nИспользуйте: <code>/admin_announce [сообщение]</code>\n\nПример: <code>/admin_announce Важное объявление!</code>\n\nОтправит объявление всем пользователям.",
        
        "admin_test_notification": "🔔 <b>Тест уведомлений</b>\n\nИспользуйте: <code>/admin_test_notification</code>\n\nОтправит тестовое уведомление всем пользователям.",
        
        "admin_event_start": "🎉 <b>Запустить событие</b>\n\nИспользуйте: <code>/admin_event_start [название] [длительность]</code>\n\nПример: <code>/admin_event_start Новогоднее событие 7</code>\n\nЗапустит событие на указанное количество дней.",
        
        "admin_event_end": "🔚 <b>Завершить событие</b>\n\nИспользуйте: <code>/admin_event_end</code>\n\nЗавершит активное событие.",
        
        "admin_give_event_rewards": "🎁 <b>Выдать награды события</b>\n\nИспользуйте: <code>/admin_give_event_rewards [событие]</code>\n\nПример: <code>/admin_give_event_rewards Новогоднее событие</code>\n\nВыдаст награды участникам события.",
        
        "admin_set_event_banner": "🎴 <b>Установить баннер события</b>\n\nИспользуйте: <code>/admin_set_event_banner [группа] [альбом]</code>\n\nПример: <code>/admin_set_event_banner BLACKPINK BORN PINK</code>\n\nУстановит баннер для активного события.",
        
        "admin_warn": "⚠️ <b>Предупреждение</b>\n\nИспользуйте: <code>/admin_warn [ID] [причина]</code>\n\nПример: <code>/admin_warn 123456789 Нарушение правил</code>\n\nОтправит предупреждение пользователю.",
        
        "admin_mute": "🔇 <b>Замутить пользователя</b>\n\nИспользуйте: <code>/admin_mute [ID] [часы]</code>\n\nПример: <code>/admin_mute 123456789 24</code>\n\nЗамутит пользователя на указанное количество часов.",
        
        "admin_unmute": "🔊 <b>Размутить пользователя</b>\n\nИспользуйте: <code>/admin_unmute [ID]</code>\n\nПример: <code>/admin_unmute 123456789</code>\n\nРазмутит пользователя.",
        
        "admin_daily_report": "📊 <b>Ежедневный отчет</b>\n\nИспользуйте: <code>/admin_daily_report</code>\n\nСгенерирует ежедневный отчет.",
        
        "admin_weekly_report": "📈 <b>Еженедельный отчет</b>\n\nИспользуйте: <code>/admin_weekly_report</code>\n\nСгенерирует еженедельный отчет.",
        
        "admin_revenue_stats": "💰 <b>Статистика доходов</b>\n\nИспользуйте: <code>/admin_revenue_stats</code>\n\nПокажет статистику доходов.",
        
        "admin_popular_cards": "🔥 <b>Популярные карточки</b>\n\nИспользуйте: <code>/admin_popular_cards [количество]</code>\n\nПример: <code>/admin_popular_cards 10</code>\n\nПокажет самые популярные карточки."
    }
    
    return command_info.get(command_name, f"ℹ️ Информация о команде {command_name} недоступна.") 