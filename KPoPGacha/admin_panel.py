from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import ADMIN_IDS
import pb_client as pb

# Состояния для ConversationHandler
ADMIN_MENU, ADD_STARS_MENU, ADD_STARS_AMOUNT, ADD_STARS_USER, GIVE_CARDS_MENU, GIVE_CARDS_USER, GIVE_CARDS_AMOUNT = range(7)

async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню админ-панели"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Доступ запрещен.")
        return ConversationHandler.END
    
    keyboard = [
        [InlineKeyboardButton("⭐ Добавить всем звезд", callback_data="admin_add_stars_all")],
        [InlineKeyboardButton("👤 Добавить звезд пользователю", callback_data="admin_add_stars_user")],
        [InlineKeyboardButton("🎴 Выдать карточки пользователю", callback_data="admin_give_cards")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("🔄 Сбросить pity всем", callback_data="admin_reset_pity")],
        [InlineKeyboardButton("❌ Отмена", callback_data="admin_cancel")]
    ]
    
    await update.message.reply_text(
        "🔧 <b>Админ-панель</b>\n\nВыберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
    return ADMIN_MENU

async def admin_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка callback'ов админ-меню"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "admin_add_stars_all":
        await query.edit_message_text(
            "⭐ <b>Добавить всем звезд</b>\n\nВведите количество звезд:",
            parse_mode="HTML"
        )
        return ADD_STARS_AMOUNT
    
    elif query.data == "admin_add_stars_user":
        await query.edit_message_text(
            "👤 <b>Добавить звезд пользователю</b>\n\nВведите Telegram ID пользователя:",
            parse_mode="HTML"
        )
        return ADD_STARS_USER
    
    elif query.data == "admin_give_cards":
        await query.edit_message_text(
            "🎴 <b>Выдать карточки пользователю</b>\n\nВведите Telegram ID пользователя:",
            parse_mode="HTML"
        )
        return GIVE_CARDS_USER
    
    elif query.data == "admin_stats":
        stats = await get_admin_stats()
        await query.edit_message_text(
            f"📊 <b>Статистика</b>\n\n{stats}",
            parse_mode="HTML"
        )
        return await show_admin_back_menu(query)
    
    elif query.data == "admin_reset_pity":
        await reset_pity_all()
        await query.edit_message_text(
            "🔄 <b>Pity сброшен для всех пользователей</b>",
            parse_mode="HTML"
        )
        return await show_admin_back_menu(query)
    
    elif query.data == "admin_cancel":
        await query.edit_message_text("❌ Операция отменена.")
        return ConversationHandler.END
    
    elif query.data == "admin_back":
        return await admin_start(update, context)

async def add_stars_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода количества звезд"""
    try:
        amount = int(update.message.text)
        if amount <= 0:
            await update.message.reply_text("❌ Количество должно быть положительным!")
            return ADD_STARS_AMOUNT
        
        # Проверяем, есть ли целевой пользователь в контексте
        target_user_id = context.user_data.get('target_user_id')
        if target_user_id:
            # Добавляем звезды конкретному пользователю
            await add_stars_to_user(target_user_id, amount)
            await update.message.reply_text(f"✅ Добавлено {amount} звезд пользователю!")
            # Очищаем контекст
            context.user_data.pop('target_user_id', None)
        else:
            # Добавляем звезды всем пользователям
            await add_stars_to_all(amount)
            await update.message.reply_text(f"✅ Добавлено {amount} звезд всем пользователям!")
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")
        return ADD_STARS_AMOUNT

async def add_stars_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода Telegram ID пользователя"""
    try:
        user_id = int(update.message.text)
        pb_user = pb.get_user_by_telegram_id(user_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return ADD_STARS_USER
        
        context.user_data['target_user_id'] = user_id
        await update.message.reply_text(
            f"👤 Пользователь найден: {pb_user.get('name', 'Неизвестно')}\n\nВведите количество звезд:"
        )
        return ADD_STARS_AMOUNT
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректный Telegram ID!")
        return ADD_STARS_USER

async def give_cards_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода Telegram ID для выдачи карточек"""
    try:
        user_id = int(update.message.text)
        pb_user = pb.get_user_by_telegram_id(user_id)
        if not pb_user:
            await update.message.reply_text("❌ Пользователь не найден!")
            return GIVE_CARDS_USER
        
        context.user_data['target_user_id'] = user_id
        await update.message.reply_text(
            f"👤 Пользователь найден: {pb_user.get('name', 'Неизвестно')}\n\nВведите количество карточек:"
        )
        return GIVE_CARDS_AMOUNT
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректный Telegram ID!")
        return GIVE_CARDS_USER

async def give_cards_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода количества карточек"""
    try:
        amount = int(update.message.text)
        if amount <= 0 or amount > 100:
            await update.message.reply_text("❌ Количество должно быть от 1 до 100!")
            return GIVE_CARDS_AMOUNT
        
        user_id = context.user_data.get('target_user_id')
        await give_random_cards(user_id, amount)
        await update.message.reply_text(f"✅ Выдано {amount} случайных карточек пользователю!")
        # Очищаем контекст
        context.user_data.pop('target_user_id', None)
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("❌ Введите корректное число!")
        return GIVE_CARDS_AMOUNT

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
    """Создать ConversationHandler для админ-панели"""
    return ConversationHandler(
        entry_points=[CommandHandler("admin", admin_start)],
        states={
            ADMIN_MENU: [CallbackQueryHandler(admin_menu_callback)],
            ADD_STARS_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_stars_amount)],
            ADD_STARS_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_stars_user)],
            GIVE_CARDS_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, give_cards_user)],
            GIVE_CARDS_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, give_cards_amount)],
        },
        fallbacks=[CommandHandler("cancel", admin_cancel)],
        per_message=False
    ) 