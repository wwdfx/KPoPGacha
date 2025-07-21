from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from pb_client import PBClient
from config import TELEGRAM_BOT_TOKEN, ADMIN_IDS
import random
import os
import tempfile
import requests
from PIL import Image
from telegram.ext import ConversationHandler, MessageHandler, filters
from collections import defaultdict
import httpx
import asyncio
from config import AUCTION_CHANNEL_ID

pb = PBClient()

# Шансы выпадения по редкости (сумма = 100)
RARITY_CHANCES = [
    (1, 40),   # 1 звезда - 29%
    (2, 32),   # 2 звезды - 30%
    (3, 20),   # 3 звезды - 25%
    (4, 5),   # 4 звезды - 12%
    (5, 2),    # 5 звёзд - 3%
    (6, 0.5),    # 6 звёзд - 0.5%
]
RARITY_WEIGHTS = [chance for _, chance in RARITY_CHANCES]
RARITY_VALUES = [rarity for rarity, _ in RARITY_CHANCES]

PULL_COST = 10  # Стоимость одной попытки в звёздах 
PULL10_COST = 90  # Стоимость 10 попыток (скидка)

ADD_NAME, ADD_GROUP, ADD_ALBUM, ADD_RARITY, ADD_IMAGE, ADD_CONFIRM = range(6)
AUCTION_PRICE, AUCTION_DURATION, AUCTION_CONFIRM = range(10, 13)
auction_data = {}

addcard_data = {}

message_counters = defaultdict(int)

PROMO_ENTER, = range(20, 21)

EXCHANGE_SELECT, EXCHANGE_CONFIRM = range(40, 42)

async def promo_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    await target.reply_text("Введите промокод:")
    return PROMO_ENTER

async def promo_enter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    promo = pb.get_promo(code)
    if not promo:
        await update.message.reply_text("❌ Промокод не найден.")
        return ConversationHandler.END
    if not promo.get("is_active", True):
        await update.message.reply_text("❌ Промокод неактивен.")
        return ConversationHandler.END
    usage_limit = promo.get("usage_limit", 1)
    used_by = promo.get("used_by", [])
    if len(used_by) >= usage_limit:
        await update.message.reply_text("❌ Превышен лимит активаций промокода.")
        return ConversationHandler.END
    if pb_user["id"] in used_by:
        await update.message.reply_text("❌ Вы уже использовали этот промокод.")
        return ConversationHandler.END
    # Выдаём награду
    reward = promo.get("reward", 0)
    pb.update_user_stars_and_pity(pb_user["id"], pb_user.get("stars", 0) + reward, pb_user.get("pity_legendary", 0), pb_user.get("pity_void", 0))
    pb.use_promo(promo["id"], pb_user["id"])
    await update.message.reply_text(f"✅ Промокод активирован! Вы получили {reward} звёзд.")
    return ConversationHandler.END

async def promo_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Ввод промокода отменён.")
    return ConversationHandler.END

# --- Админ-команда для добавления промокода ---
ADD_PROMO_CODE, ADD_PROMO_REWARD, ADD_PROMO_LIMIT = range(30, 33)
addpromo_data = {}

async def addpromo_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Только для администратора.")
        return ConversationHandler.END
    addpromo_data[user_id] = {}
    await update.message.reply_text("Введите промокод (только латиница/цифры):")
    return ADD_PROMO_CODE

async def addpromo_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addpromo_data[user_id]["code"] = update.message.text.strip()
    await update.message.reply_text("Введите награду (сколько звёзд):")
    return ADD_PROMO_REWARD

async def addpromo_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        reward = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Введите число!")
        return ADD_PROMO_REWARD
    addpromo_data[user_id]["reward"] = reward
    await update.message.reply_text("Введите лимит использований (число, 0 = безлимит):")
    return ADD_PROMO_LIMIT

async def addpromo_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        limit = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Введите число!")
        return ADD_PROMO_LIMIT
    addpromo_data[user_id]["usage_limit"] = limit if limit > 0 else 1000000
    data = addpromo_data[user_id]
    pb.add_promo(data["code"], data["reward"], data["usage_limit"], True)
    await update.message.reply_text(f"✅ Промокод {data['code']} добавлен! Награда: {data['reward']} звёзд, лимит: {data['usage_limit']}")
    addpromo_data.pop(user_id, None)
    return ConversationHandler.END

async def addpromo_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addpromo_data.pop(user_id, None)
    await update.message.reply_text("❌ Добавление промокода отменено.")
    return ConversationHandler.END

def get_reply_target(update, prefer_edit=False):
    if prefer_edit and hasattr(update, 'callback_query') and update.callback_query and update.callback_query.message:
        return update.callback_query.message
    if hasattr(update, 'message') and update.message:
        return update.message
    elif hasattr(update, 'callback_query') and update.callback_query and update.callback_query.message:
        return update.callback_query.message
    return None

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="menu")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        pb.create_user(user.id, user.full_name)
        if target:
            await target.reply_text(f"👋 Добро пожаловать, <b>{user.full_name}</b>!\nВаш игровой профиль создан.", parse_mode="HTML")
    else:
        if target:
            await target.reply_text(f"✨ С возвращением, <b>{user.full_name}</b>!", parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    if target:
        await target.reply_text(
            "<b>Доступные команды:</b>\n"
            "<b>/menu</b> — главное меню\n"
            "<b>/profile</b> — ваш профиль\n"
            "<b>/pull</b> — гача (1 попытка)\n"
            "<b>/pull10</b> — гача (10 попыток)\n"
            "<b>/inventory</b> — коллекция\n"
            "<b>/daily</b> — ежедневка\n"
            "<b>/history</b> — история попыток\n"
            "<b>/pity</b> — pity-счётчики\n"
            "<b>/leaderboard</b> — топ игроков\n"
            "<b>/settings</b> — настройки\n"
            "<b>/help</b> — помощь",
            parse_mode="HTML"
        )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    rank = pb.get_rank(pb_user.get('level', 1))
    text = (
        f"<b>👤 Профиль:</b>\n"
        f"<b>Имя:</b> {pb_user.get('name', '')}\n"
        f"<b>Уровень:</b> {pb_user.get('level', 1)} <i>({rank})</i>\n"
        f"<b>Опыт:</b> {pb_user.get('exp', 0)} / {pb.exp_to_next_level(pb_user.get('level', 1))}\n"
        f"<b>⭐ Звёзды:</b> {pb_user.get('stars', 0)}\n"
        f"<b>🎯 Pity Legendary:</b> {pb_user.get('pity_legendary', 0)} / 80\n"
        f"<b>🕳️ Pity Void:</b> {pb_user.get('pity_void', 0)} / 165"
    )
    if target:
        if prefer_edit:
            await target.edit_text(text, parse_mode="HTML", reply_markup=back_keyboard())
        else:
            await target.reply_text(text, parse_mode="HTML", reply_markup=back_keyboard())

# --- Гача логика ---
def choose_rarity(pity_legendary, pity_void):
    # Pity: 80 - гарант 5*, 165 - гарант 6*
    if pity_void >= 165:
        return 6
    if pity_legendary >= 80:
        return 5
    return random.choices(RARITY_VALUES, weights=RARITY_WEIGHTS, k=1)[0]

def apply_overlay(card_image_url, rarity):
    if rarity not in (3, 4, 5, 6):
        return None  # Эффект только для 3★ и выше
    overlay_path = os.path.join(os.path.dirname(__file__), "overlays", f"overlay_{rarity}.png")
    if not os.path.exists(overlay_path):
        return None  # Нет оверлея для этой редкости
    # Скачиваем картинку карточки
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_card:
        resp = requests.get(card_image_url)
        temp_card.write(resp.content)
        temp_card_path = temp_card.name
    # Открываем изображения
    card_img = Image.open(temp_card_path).convert("RGBA")
    overlay_img = Image.open(overlay_path).convert("RGBA")
    # Масштабируем оверлей под размер карточки
    overlay_img = overlay_img.resize(card_img.size, Image.Resampling.LANCZOS)
    # Накладываем оверлей
    combined = Image.alpha_composite(card_img, overlay_img)
    # Сохраняем результат
    out_path = tempfile.mktemp(suffix=".png")
    combined.save(out_path, format="PNG")
    os.unlink(temp_card_path)
    return out_path

async def pull_once(user, pb_user, update, pull_type="single"):
    target = get_reply_target(update)
    pity_legendary = pb_user.get("pity_legendary", 0)
    pity_void = pb_user.get("pity_void", 0)
    stars = pb_user.get("stars", 0)
    user_id = pb_user["id"]
    level = pb_user.get("level", 1)
    exp = pb_user.get("exp", 0)

    if stars < PULL_COST:
        if target:
            await target.reply_text("<b>Недостаточно звёзд для попытки!</b>", parse_mode="HTML")
        return

    rarity = choose_rarity(pity_legendary, pity_void)
    card = pb.get_random_card_by_rarity(rarity)
    if not card:
        if target:
            await target.reply_text(f"Нет карточек с редкостью {rarity}★ в базе!", parse_mode="HTML")
        return

    # Pity-счётчики
    if rarity == 6:
        pity_void = 0
        pity_legendary += 1
    elif rarity == 5:
        pity_legendary = 0
        pity_void += 1
    else:
        pity_legendary += 1
        pity_void += 1

    # Списываем звёзды
    stars -= PULL_COST
    pb.update_user_stars_and_pity(user_id, stars, pity_legendary, pity_void)
    pb.add_card_to_user(user_id, card["id"])
    pb.add_pull_history(user_id, card["id"], pull_type)

    # Опыт за карточку
    base_exp = PBClient.RARITY_EXP.get(card["rarity"], 1)
    is_first = pb.is_first_card(user_id, card["id"])
    total_exp = base_exp + (base_exp // 2 if is_first else 0)
    updated_user, levelup = pb.add_exp_and_check_levelup(user_id, level, exp, total_exp)

    # Ответ пользователю
    text = f"<b>Выпала карта:</b> <b>{card['name']}</b> (<i>{card['group']}</i>)\n<b>Редкость:</b> <b>{card['rarity']}★</b>\n<b>+{base_exp} опыта</b>"
    if is_first:
        text += " <i>(первое получение, бонус +50%)</i>"
    if levelup:
        rank = pb.get_rank(updated_user.get('level', 1))
        text += f"\n<b>Поздравляем! Ваш уровень повышен: {updated_user.get('level', 1)} ({rank})</b>"
    if card.get("image_url"):
        overlayed_path = apply_overlay(card["image_url"], card["rarity"])
        if overlayed_path:
            with open(overlayed_path, "rb") as img_file:
                await target.reply_photo(img_file, caption=text, parse_mode="HTML")
            os.unlink(overlayed_path)
        else:
            await target.reply_photo(card["image_url"], caption=text, parse_mode="HTML")
    else:
        if target:
            await target.reply_text(text, parse_mode="HTML")

async def pull(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await pull_once(update.effective_user, pb.get_user_by_telegram_id(update.effective_user.id), update, pull_type="single")

async def pull10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await pull10_impl(update.effective_user, pb.get_user_by_telegram_id(update.effective_user.id), update)

async def pull10_impl(user, pb_user, update):
    target = get_reply_target(update)
    stars = pb_user.get("stars", 0)
    if stars < PULL10_COST:
        if target:
            await target.reply_text("<b>Недостаточно звёзд для 10 попыток!</b>", parse_mode="HTML")
        return
    user_id = pb_user["id"]
    pity_legendary = pb_user.get("pity_legendary", 0)
    pity_void = pb_user.get("pity_void", 0)
    level = pb_user.get("level", 1)
    exp = pb_user.get("exp", 0)
    stars -= PULL10_COST
    results = ["<b>Результаты 10 попыток:</b>"]
    total_exp = 0
    levelup = False
    media = []
    captions = []
    for i in range(10):
        rarity = choose_rarity(pity_legendary, pity_void)
        card = pb.get_random_card_by_rarity(rarity)
        if not card:
            results.append(f"{i+1}. Нет карточек с редкостью {rarity}★!")
            continue
        if rarity == 6:
            pity_void = 0
            pity_legendary += 1
        elif rarity == 5:
            pity_legendary = 0
            pity_void += 1
        else:
            pity_legendary += 1
            pity_void += 1
        pb.add_card_to_user(user_id, card["id"])
        pb.add_pull_history(user_id, card["id"], "multi")
        base_exp = PBClient.RARITY_EXP.get(card["rarity"], 1)
        is_first = pb.is_first_card(user_id, card["id"])
        exp_gain = base_exp + (base_exp // 2 if is_first else 0)
        total_exp += exp_gain
        caption = (
            f"<b>{card['name']}</b> (<i>{card['group']}</i>)\n"
            f"Альбом: <b>{card.get('album', '-')}</b>\n"
            f"Редкость: <b>{card['rarity']}★</b> <b>+{exp_gain} опыта</b>"
        )
        if is_first:
            caption += " <i>(первое получение)</i>"
        overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
        if overlayed_path:
            media.append(InputMediaPhoto(open(overlayed_path, "rb"), caption=caption, parse_mode="HTML"))
            captions.append(overlayed_path)
        elif card.get("image_url"):
            media.append(InputMediaPhoto(card["image_url"], caption=caption, parse_mode="HTML"))
            captions.append(None)
        else:
            results.append(f"{i+1}. {card['name']} — нет изображения")
    updated_user, levelup = pb.add_exp_and_check_levelup(user_id, level, exp, total_exp)
    pb.update_user_stars_and_pity(user_id, stars, pity_legendary, pity_void)
    if levelup:
        rank = pb.get_rank(updated_user.get('level', 1))
        results.append(f"\n<b>Поздравляем! Ваш уровень повышен: {updated_user.get('level', 1)} ({rank})</b>")
    # Отправляем альбом, если есть хотя бы 2 картинки
    if media:
        try:
            await target.reply_media_group(media)
        except Exception:
            # Если не поддерживается альбом — отправляем по одной
            for m in media:
                await target.reply_photo(m.media, caption=m.caption, parse_mode="HTML")
        # Чистим временные файлы
        for path in captions:
            if path:
                try:
                    os.unlink(path)
                except Exception:
                    pass
    if results and len(results) > 1:
        await target.reply_text("\n".join(results), parse_mode="HTML")

# --- Новый инвентарь: группировка по группам и альбомам ---
async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    user_id = pb_user["id"]
    cards = pb.get_user_inventory(user_id)
    if not cards:
        if target:
            if prefer_edit:
                await target.edit_text("Ваша коллекция пуста!", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Ваша коллекция пуста!", parse_mode="HTML", reply_markup=back_keyboard())
        return
    # Группируем по группам
    group_set = set()
    for c in cards:
        card = c.get("expand", {}).get("card_id", {})
        if not card:
            continue
        group = card.get("group", "-")
        group_set.add(group)
    keyboard = []
    for group in sorted(group_set):
        keyboard.append([InlineKeyboardButton(f"{group}", callback_data=f"invgroup_{group}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="menu")])
    text = "<b>🎴 Ваша коллекция:</b>\nВыберите группу:"
    if target:
        if prefer_edit:
            await target.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        else:
            await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- Callback: выбор группы, затем альбома ---
async def inventory_group_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group = query.data.replace("invgroup_", "")
    user_id = query.from_user.id
    pb_user = pb.get_user_by_telegram_id(user_id)
    cards = pb.get_user_inventory(pb_user["id"])
    # Группируем по альбомам внутри выбранной группы
    album_set = set()
    for c in cards:
        card = c.get("expand", {}).get("card_id", {})
        if not card:
            continue
        if card.get("group", "-") == group:
            album_set.add(card.get("album", "-"))
    keyboard = []
    for album in sorted(album_set):
        keyboard.append([InlineKeyboardButton(f"{album}", callback_data=f"invalbum_{group}__{album}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="inventory")])
    text = f"<b>Группа:</b> <b>{group}</b>\nВыберите альбом:"
    try:
        if query.message:
            if query.message.photo:
                await query.message.edit_caption(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

# --- Callback: выбор альбома, затем карточки ---
async def inventory_album_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.replace("invalbum_", "")
    group, album = data.split("__", 1)
    user_id = query.from_user.id
    pb_user = pb.get_user_by_telegram_id(user_id)
    cards = pb.get_user_inventory(pb_user["id"])
    # Список карточек в выбранном альбоме и группе, сортировка по редкости (от 6 до 1)
    filtered_cards = [
        c for c in cards
        if c.get("expand", {}).get("card_id", {}).get("group", "-") == group and c.get("expand", {}).get("card_id", {}).get("album", "-") == album
    ]
    # Сортируем по убыванию редкости
    filtered_cards.sort(key=lambda c: c.get("expand", {}).get("card_id", {}).get("rarity", 1), reverse=True)
    card_buttons = []
    for c in filtered_cards:
        card = c.get("expand", {}).get("card_id", {})
        btn_text = f"{card.get('name', '???')} — {card.get('rarity', '?')}★ ×{c.get('count', 1)}"
        card_buttons.append([InlineKeyboardButton(btn_text, callback_data=f"showcard_{card.get('id')}")])
    card_buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data=f"invgroup_{group}")])
    text = f"<b>Группа:</b> <b>{group}</b>\n<b>Альбом:</b> <b>{album}</b>\nВыберите карточку:"
    try:
        if query.message:
            if query.message.photo:
                await query.message.edit_caption(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(card_buttons))
            else:
                await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(card_buttons))
        else:
            await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(card_buttons))
    except Exception:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(card_buttons))

async def showcard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = query.data.replace("showcard_", "")
    url = f"{pb.base_url}/collections/cards/records/{card_id}"
    resp = requests.get(url, headers=pb.headers)
    if resp.status_code != 200:
        await query.edit_message_text("Карточка не найдена.")
        return
    card = resp.json()
    user_id = query.from_user.id
    user_cards = pb.get_user_inventory(pb.get_user_by_telegram_id(user_id)["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    count = user_card.get("count", 0) if user_card else 0
    can_auction = count > 0
    text = (
        f"<b>{card.get('name')}</b>\n"
        f"Группа: <b>{card.get('group')}</b>\n"
        f"Альбом: <b>{card.get('album', '-')}</b>\n"
        f"Редкость: <b>{card.get('rarity')}★</b>\n"
        f"В наличии: <b>{count}</b>"
    )
    keyboard = []
    if can_auction:
        keyboard.append([InlineKeyboardButton("💸 Выложить на аукцион", callback_data=f"auction_{card_id}")])
    # Кнопка сдачи дубликатов
    if count > 1:
        keyboard.append([InlineKeyboardButton(f"♻️ Сдать дубликат ({count-1})", callback_data=f"exchange_{card_id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="inventory")])
    overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
    if overlayed_path:
        with open(overlayed_path, "rb") as img_file:
            await query.message.reply_photo(img_file, caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        os.unlink(overlayed_path)
    elif card.get("image_url"):
        await query.message.reply_photo(card.get("image_url"), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def auction_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = query.data.replace("auction_", "")
    user_id = query.from_user.id
    auction_data[user_id] = {"card_id": card_id}
    await query.message.reply_text("Введите цену в звёздах:")
    return AUCTION_PRICE

async def auction_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        price = int(update.message.text.strip())
        if price < 1:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Введите положительное число!")
        return AUCTION_PRICE
    auction_data[user_id]["price"] = price
    # Показываем кнопки для выбора срока
    keyboard = [
        [InlineKeyboardButton("12 ч", callback_data="auction_dur_12"),
         InlineKeyboardButton("24 ч", callback_data="auction_dur_24"),
         InlineKeyboardButton("48 ч", callback_data="auction_dur_48")]
    ]
    await update.message.reply_text("Выберите срок аукциона:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AUCTION_DURATION

async def auction_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if query.data.startswith("auction_dur_"):
        hours = int(query.data.split("_")[-1])
        auction_data[user_id]["duration"] = hours
        data = auction_data[user_id]
        text = f"Выставить карточку на аукцион за {data['price']} звёзд на {hours} ч?"
        keyboard = [[InlineKeyboardButton("✅ Да", callback_data="auction_yes"), InlineKeyboardButton("❌ Нет", callback_data="auction_no")]]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return AUCTION_CONFIRM
    await query.message.reply_text("Ошибка выбора срока.")
    return ConversationHandler.END

async def auction_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if query.data == "auction_no":
        await query.edit_message_text("❌ Выставление отменено.")
        auction_data.pop(user_id, None)
        return ConversationHandler.END
    data = auction_data[user_id]
    pb_user = pb.get_user_by_telegram_id(user_id)
    # Уменьшаем count карточки у пользователя
    user_cards = pb.get_user_inventory(pb_user["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == data["card_id"] or (c.get("expand", {}).get("card_id", {}).get("id") == data["card_id"])), None)
    if user_card and user_card.get("count", 0) > 0:
        url = f"{pb.base_url}/collections/user_cards/records/{user_card['id']}"
        new_count = user_card.get("count", 1) - 1
        httpx.patch(url, headers=pb.headers, json={"count": new_count})
    pb.create_auction(data["card_id"], pb_user["id"], data["price"], data["duration"])
    await query.edit_message_text("✅ Карточка выставлена на аукцион!")
    # Отправка уведомления в канал о новом аукционе
    if AUCTION_CHANNEL_ID:
        card = pb.get_card(data["card_id"])
        text = (
            f"<b>Новый аукцион!</b>\n"
            f"Карточка: <b>{card.get('name', '???')}</b> ({card.get('group', '-')})\n"
            f"Альбом: <b>{card.get('album', '-')}</b>\n"
            f"Редкость: <b>{card.get('rarity', '?')}★</b>\n"
            f"Цена: <b>{data['price']}⭐</b>\n"
            f"Срок: <b>{data['duration']} ч</b>\n"
            f"Продавец: <b>{pb_user.get('name', '-')[:20]}</b>"
        )
        try:
            if card.get("image_url"):
                await context.bot.send_photo(
                    chat_id=AUCTION_CHANNEL_ID,
                    photo=card["image_url"],
                    caption=text,
                    parse_mode="HTML"
                )
            else:
                await context.bot.send_message(
                    chat_id=AUCTION_CHANNEL_ID,
                    text=text,
                    parse_mode="HTML"
                )
        except Exception as e:
            print(f"[AUCTION CHANNEL ERROR] {e}")
    auction_data.pop(user_id, None)
    return ConversationHandler.END

async def auctions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    auctions = pb.get_active_auctions()
    if not auctions:
        keyboard = [[InlineKeyboardButton("🎴 Инвентарь", callback_data="inventory")]]
        text = "Нет активных лотов. Вы можете выложить свою карточку на аукцион через инвентарь!"
        if prefer_edit:
            await target.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    keyboard = []
    for lot in auctions:
        card = lot.get("expand", {}).get("card_id", {})
        seller = lot.get("expand", {}).get("seller_id", {})
        btn_text = f"{card.get('name', '???')} ({card.get('group', '-')}) — {card.get('rarity', '?')}★ за {lot.get('price')}⭐ от {seller.get('name', '-')[:12]}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"buyauction_{lot['id']}")])
    text = "<b>Аукцион:</b>"
    if prefer_edit:
        await target.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def buyauction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lot_id = query.data.replace("buyauction_", "")
    lot = pb.get_auction(lot_id)
    card = lot.get("expand", {}).get("card_id", {})
    price = lot.get("price")
    buyer_id = query.from_user.id
    pb_buyer = pb.get_user_by_telegram_id(buyer_id)
    if pb_buyer.get("stars", 0) < price:
        await query.edit_message_text("Недостаточно звёзд!")
        return
    # Списываем звёзды у покупателя, начисляем продавцу, добавляем карточку покупателю
    pb.update_user_stars_and_pity(pb_buyer["id"], pb_buyer["stars"] - price, pb_buyer.get("pity_legendary", 0), pb_buyer.get("pity_void", 0))
    seller = lot.get("expand", {}).get("seller_id", {})
    if seller:
        pb_seller = pb.get_user_by_telegram_id(seller.get("telegram_id"))
        if pb_seller:
            pb.update_user_stars_and_pity(pb_seller["id"], pb_seller.get("stars", 0) + price, pb_seller.get("pity_legendary", 0), pb_seller.get("pity_void", 0))
            # Уведомление продавцу
            seller_tg_id = seller.get("telegram_id")
            if seller_tg_id:
                try:
                    await context.bot.send_message(
                        chat_id=int(seller_tg_id),
                        text=f"💸 Ваша карточка <b>{card.get('name')}</b> была куплена за <b>{price} звёзд</b>!",
                        parse_mode="HTML"
                    )
                except Exception:
                    pass
    pb.add_card_to_user(pb_buyer["id"], card["id"])
    pb.finish_auction(lot_id, status="sold", winner_id=pb_buyer["id"])
    await query.edit_message_text(f"✅ Покупка успешна! Карточка {card.get('name')} теперь ваша.")

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    available, last_dt = pb.check_daily_available(pb_user)
    if not available:
        if target:
            if prefer_edit:
                await target.edit_text("<b>Вы уже получали ежедневную награду сегодня! Возвращайтесь завтра.</b>", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("<b>Вы уже получали ежедневную награду сегодня! Возвращайтесь завтра.</b>", parse_mode="HTML", reply_markup=back_keyboard())
        return
    user_id = pb_user["id"]
    stars = pb_user.get("stars", 0)
    updated_user, reward = pb.give_daily_reward(user_id, stars)
    if target:
        if prefer_edit:
            await target.edit_text(f"<b>🎁 Вы получили {reward} звёзд за ежедневный вход!</b>\nДо встречи завтра ✨", parse_mode="HTML", reply_markup=back_keyboard())
        else:
            await target.reply_text(f"<b>🎁 Вы получили {reward} звёзд за ежедневный вход!</b>\nДо встречи завтра ✨", parse_mode="HTML", reply_markup=back_keyboard())

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    user_id = pb_user["id"]
    pulls = pb.get_pull_history(user_id, limit=10)
    if not pulls:
        if target:
            if prefer_edit:
                await target.edit_text("История пуста.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("История пуста.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    lines = ["<b>🕓 Последние попытки:</b>"]
    for p in pulls:
        card = p.get("expand", {}).get("card_id", {})
        if not card:
            continue
        lines.append(f"<b>{card.get('name', '???')}</b> (<i>{card.get('group', '-')}</i>) — <b>{card.get('rarity', '?')}★</b> [<i>{p.get('pull_type', '')}</i>]")
    if target:
        if prefer_edit:
            await target.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_keyboard())
        else:
            await target.reply_text("\n".join(lines), parse_mode="HTML", reply_markup=back_keyboard())

async def pity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    user_id = pb_user["id"]
    pity_legendary, pity_void = pb.get_pity_status(user_id)
    if target:
        if prefer_edit:
            await target.edit_text(f"<b>🎯 Pity Legendary:</b> {pity_legendary}/80\n<b>🕳️ Pity Void:</b> {pity_void}/165", parse_mode="HTML", reply_markup=back_keyboard())
        else:
            await target.reply_text(f"<b>🎯 Pity Legendary:</b> {pity_legendary}/80\n<b>🕳️ Pity Void:</b> {pity_void}/165", parse_mode="HTML", reply_markup=back_keyboard())

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    top = pb.get_leaderboard(limit=10)
    if not top:
        if target:
            if prefer_edit:
                await target.edit_text("Лидерборд пуст.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Лидерборд пуст.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    lines = ["<b>🏆 Топ коллекционеров:</b>"]
    for i, user in enumerate(top, 1):
        name = user.get("name") or f"User {user.get('telegram_id', '')}" 
        level = user.get("level", 1)
        exp = user.get("exp", 0)
        rank = pb.get_rank(level)
        lines.append(f"{i}. <b>{name}</b> — <b>{level}</b> <i>({rank})</i>, опыт: <b>{exp}</b>")
    if target:
        if prefer_edit:
            await target.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_keyboard())
        else:
            await target.reply_text("\n".join(lines), parse_mode="HTML", reply_markup=back_keyboard())

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    if target:
        if prefer_edit:
            await target.edit_text("<b>⚙️ Настройки профиля будут доступны в будущих обновлениях.</b>", parse_mode="HTML", reply_markup=back_keyboard())
        else:
            await target.reply_text("<b>⚙️ Настройки профиля будут доступны в будущих обновлениях.</b>", parse_mode="HTML", reply_markup=back_keyboard())

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    keyboard = [
        [InlineKeyboardButton("👤 Профиль", callback_data="profile"), InlineKeyboardButton("🎴 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton("🎲 Гача (1)", callback_data="pull"), InlineKeyboardButton("🔟 Гача (10)", callback_data="pull10")],
        [InlineKeyboardButton("🎁 Ежедневка", callback_data="daily"), InlineKeyboardButton("🕓 История", callback_data="history")],
        [InlineKeyboardButton("🎯 Pity", callback_data="pity"), InlineKeyboardButton("🏆 Лидерборд", callback_data="leaderboard")],
        [InlineKeyboardButton("🛒 Аукцион", callback_data="auctions")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = get_reply_target(update, prefer_edit=prefer_edit)
    if target:
        if prefer_edit:
            await target.edit_text("<b>Главное меню:</b>", reply_markup=reply_markup, parse_mode="HTML")
        else:
            await target.reply_text("<b>Главное меню:</b>", reply_markup=reply_markup, parse_mode="HTML")

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    # Добавлено: обработка кнопки 'Назад' (data == 'menu')
    if data == "menu":
        await menu(update, context)
        return
    if data == "profile":
        await profile(update, context)
    elif data == "inventory":
        await inventory(update, context)
    elif data == "pull":
        await pull(update, context)
    elif data == "pull10":
        await pull10(update, context)
    elif data == "daily":
        await daily(update, context)
    elif data == "history":
        await history(update, context)
    elif data == "pity":
        await pity(update, context)
    elif data == "leaderboard":
        await leaderboard(update, context)
    elif data == "settings":
        await settings(update, context)
    elif data == "auctions":
        await auctions(update, context)
    else:
        await query.edit_message_text("Неизвестная команда.")

async def addcard_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Только для администратора.")
        return ConversationHandler.END
    addcard_data[user_id] = {}
    await update.message.reply_text("Введите <b>имя карточки</b>:", parse_mode="HTML")
    return ADD_NAME

async def addcard_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addcard_data[user_id]["name"] = update.message.text.strip()
    await update.message.reply_text("Введите <b>группу</b>:", parse_mode="HTML")
    return ADD_GROUP

async def addcard_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addcard_data[user_id]["group"] = update.message.text.strip()
    await update.message.reply_text("Введите <b>название альбома</b>:", parse_mode="HTML")
    return ADD_ALBUM

async def addcard_album(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addcard_data[user_id]["album"] = update.message.text.strip()
    await update.message.reply_text("Введите <b>редкость</b> (1-6):", parse_mode="HTML")
    return ADD_RARITY

async def addcard_rarity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        rarity = int(update.message.text.strip())
        if rarity < 1 or rarity > 6:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Введите число от 1 до 6!")
        return ADD_RARITY
    addcard_data[user_id]["rarity"] = rarity
    await update.message.reply_text("Вставьте <b>URL изображения</b>:", parse_mode="HTML")
    return ADD_IMAGE

async def addcard_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addcard_data[user_id]["image_url"] = update.message.text.strip()
    card = addcard_data[user_id]
    text = (
        f"<b>Проверьте данные:</b>\n"
        f"Имя: {card['name']}\nГруппа: {card['group']}\nАльбом: {card['album']}\nРедкость: {card['rarity']}\nURL: {card['image_url']}\n\nДобавить эту карточку?"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data="addcard_yes"), InlineKeyboardButton("❌ Нет", callback_data="addcard_no")]
    ]
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    return ADD_CONFIRM

async def addcard_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if query.data == "addcard_no":
        await query.edit_message_text("❌ Добавление карточки отменено.")
        addcard_data.pop(user_id, None)
        return ConversationHandler.END
    card = addcard_data[user_id]
    try:
        pb.add_card(card["name"], card["group"], card["album"], card["rarity"], card["image_url"])
        await query.edit_message_text("✅ Карточка добавлена в базу!")
    except Exception as e:
        await query.edit_message_text(f"Ошибка: {e}")
    addcard_data.pop(user_id, None)
    return ConversationHandler.END

async def addcard_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    addcard_data.pop(user_id, None)
    await update.message.reply_text("❌ Добавление карточки отменено.")
    return ConversationHandler.END

async def group_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    key = (chat_id, user_id)
    message_counters[key] += 1
    if message_counters[key] % 50 == 0:
        pb_user = pb.get_user_by_telegram_id(user_id)
        if pb_user:
            new_stars = pb_user.get("stars", 0) + 25
            pb.update_user_stars_and_pity(pb_user["id"], new_stars, pb_user.get("pity_legendary", 0), pb_user.get("pity_void", 0))
            await update.message.reply_text(f"🎉 @{update.effective_user.username or update.effective_user.first_name}, вы получили 25 звёзд за активность в чате!")

# --- Новый callback для обмена дубликатов ---
async def exchange_duplicate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = query.data.replace("exchange_", "")
    user_id = query.from_user.id
    user = pb.get_user_by_telegram_id(user_id)
    user_cards = pb.get_user_inventory(user["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    count = user_card.get("count", 0) if user_card else 0
    card = user_card.get("expand", {}).get("card_id", {}) if user_card else {}
    rarity = card.get("rarity", 1)
    reward_map = {1: 1, 2: 3, 3: 10, 4: 30, 5: 100, 6: 250}
    reward = reward_map.get(rarity, 1)
    if count <= 1:
        text = "У вас нет дубликатов этой карточки."
        try:
            if query.message.photo:
                await query.message.edit_caption(text)
            else:
                await query.edit_message_text(text)
        except Exception as e:
            try:
                await query.message.reply_text(text)
            except Exception as e2:
                print(f"[exchange_duplicate_callback] Ошибка: {e} | {e2}")
        return ConversationHandler.END
    # Выбор количества дубликатов для обмена
    keyboard = []
    for i in range(1, min(count, 10)+1):
        keyboard.append([InlineKeyboardButton(f"{i}", callback_data=f"exchange_select_{card_id}_{i}")])
    keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data=f"showcard_{card_id}")])
    text = f"Сколько дубликатов <b>{card.get('name', '?')}</b> ({rarity}★) вы хотите сдать? (Доступно: {count-1})"
    try:
        if query.message.photo:
            await query.message.edit_caption(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    return EXCHANGE_SELECT

async def exchange_select_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.replace("exchange_select_", "")
    card_id, amount = data.rsplit("_", 1)
    amount = int(amount)
    user_id = query.from_user.id
    user = pb.get_user_by_telegram_id(user_id)
    user_cards = pb.get_user_inventory(user["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    count = user_card.get("count", 0) if user_card else 0
    card = user_card.get("expand", {}).get("card_id", {}) if user_card else {}
    rarity = card.get("rarity", 1)
    reward_map = {1: 1, 2: 3, 3: 10, 4: 30, 5: 100, 6: 250}
    reward = reward_map.get(rarity, 1)
    if count <= 1 or amount < 1 or amount > (count-1):
        try:
            if query.message.photo:
                await query.message.edit_caption("Некорректное количество для обмена.")
            else:
                await query.edit_message_text("Некорректное количество для обмена.")
        except Exception:
            await query.message.reply_text("Некорректное количество для обмена.")
        return ConversationHandler.END
    context.user_data["exchange"] = {"card_id": card_id, "amount": amount, "reward": reward, "rarity": rarity, "name": card.get("name", "?")}
    text = f"Вы уверены, что хотите сдать <b>{amount}</b> дубликатов <b>{card.get('name', '?')}</b> ({rarity}★) за <b>{reward*amount} звёзд</b>?\nОстанется: {count-amount}"
    keyboard = [
        [InlineKeyboardButton(f"✅ Да, сдать {amount}", callback_data=f"exchange_confirm_bulk_{card_id}_{amount}"), InlineKeyboardButton("❌ Отмена", callback_data=f"showcard_{card_id}")]
    ]
    try:
        if query.message.photo:
            await query.message.edit_caption(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    return EXCHANGE_CONFIRM

async def exchange_confirm_bulk_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.replace("exchange_confirm_bulk_", "")
    card_id, amount = data.rsplit("_", 1)
    amount = int(amount)
    user_id = query.from_user.id
    user = pb.get_user_by_telegram_id(user_id)
    user_cards = pb.get_user_inventory(user["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    count = user_card.get("count", 0) if user_card else 0
    card = user_card.get("expand", {}).get("card_id", {}) if user_card else {}
    rarity = card.get("rarity", 1)
    reward_map = {1: 1, 2: 3, 3: 10, 4: 30, 5: 100, 6: 250}
    reward = reward_map.get(rarity, 1)
    if count <= 1 or amount < 1 or amount > (count-1):
        try:
            if query.message.photo:
                await query.message.edit_caption("Некорректное количество для обмена.")
            else:
                await query.edit_message_text("Некорректное количество для обмена.")
        except Exception:
            await query.message.reply_text("Некорректное количество для обмена.")
        return ConversationHandler.END
    url = f"{pb.base_url}/collections/user_cards/records/{user_card['id']}"
    httpx.patch(url, headers=pb.headers, json={"count": count-amount})
    await asyncio.sleep(0.3)
    pb.update_user_stars_and_pity(user["id"], user.get("stars", 0) + reward*amount, user.get("pity_legendary", 0), user.get("pity_void", 0))
    text = f"♻️ Обмен завершён! Вы получили <b>{reward*amount} звёзд</b>. Осталось: {count-amount}"
    try:
        if query.message.photo:
            await query.message.edit_caption(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ К карточке", callback_data=f"showcard_refresh_{card_id}")]]))
        else:
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ К карточке", callback_data=f"showcard_refresh_{card_id}")]]))
    except Exception:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ К карточке", callback_data=f"showcard_refresh_{card_id}")]]))
    context.user_data.pop("exchange", None)
    return ConversationHandler.END

# --- Новый callback для обновления карточки после обмена ---
async def showcard_refresh_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # То же, что showcard_callback, но всегда делает свежий запрос к базе
    query = update.callback_query
    await query.answer()
    card_id = query.data.replace("showcard_refresh_", "")
    url = f"{pb.base_url}/collections/cards/records/{card_id}"
    resp = requests.get(url, headers=pb.headers)
    if resp.status_code != 200:
        await query.edit_message_text("Карточка не найдена.")
        return
    card = resp.json()
    user_id = query.from_user.id
    user_cards = pb.get_user_inventory(pb.get_user_by_telegram_id(user_id)["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    count = user_card.get("count", 0) if user_card else 0
    can_auction = count > 0
    text = (
        f"<b>{card.get('name')}</b>\n"
        f"Группа: <b>{card.get('group')}</b>\n"
        f"Альбом: <b>{card.get('album', '-')}</b>\n"
        f"Редкость: <b>{card.get('rarity')}★</b>\n"
        f"В наличии: <b>{count}</b>"
    )
    keyboard = []
    if can_auction:
        keyboard.append([InlineKeyboardButton("💸 Выложить на аукцион", callback_data=f"auction_{card_id}")])
    if count > 1:
        keyboard.append([InlineKeyboardButton(f"♻️ Сдать дубликат ({count-1})", callback_data=f"exchange_{card_id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="inventory")])
    overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
    if overlayed_path:
        with open(overlayed_path, "rb") as img_file:
            await query.message.reply_photo(img_file, caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        os.unlink(overlayed_path)
    elif card.get("image_url"):
        await query.message.reply_photo(card.get("image_url"), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("pull", pull))
    app.add_handler(CommandHandler("pull10", pull10))
    app.add_handler(CommandHandler("inventory", inventory))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("pity", pity))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("auctions", auctions))
    addcard_conv = ConversationHandler(
        entry_points=[CommandHandler("addcard", addcard_start)],
        states={
            ADD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcard_name)],
            ADD_GROUP: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcard_group)],
            ADD_ALBUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcard_album)],
            ADD_RARITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcard_rarity)],
            ADD_IMAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcard_image)],
            ADD_CONFIRM: [CallbackQueryHandler(addcard_confirm, pattern="^addcard_(yes|no)$")],
        },
        fallbacks=[CommandHandler("cancel", addcard_cancel)],
    )
    auction_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(auction_start_callback, pattern="^auction_")],
        states={
            AUCTION_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, auction_price)],
            AUCTION_DURATION: [CallbackQueryHandler(auction_duration, pattern="^auction_dur_\\d+")],
            AUCTION_CONFIRM: [CallbackQueryHandler(auction_confirm, pattern="^auction_(yes|no)$")],
        },
        fallbacks=[],
    )
    promo_conv = ConversationHandler(
        entry_points=[CommandHandler("promo", promo_start)],
        states={
            PROMO_ENTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, promo_enter)],
        },
        fallbacks=[CommandHandler("cancel", promo_cancel)],
    )
    addpromo_conv = ConversationHandler(
        entry_points=[CommandHandler("addpromo", addpromo_start)],
        states={
            ADD_PROMO_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, addpromo_code)],
            ADD_PROMO_REWARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, addpromo_reward)],
            ADD_PROMO_LIMIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, addpromo_limit)],
        },
        fallbacks=[CommandHandler("cancel", addpromo_cancel)],
    )
    exchange_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(exchange_duplicate_callback, pattern="^exchange_")],
        states={
            EXCHANGE_SELECT: [CallbackQueryHandler(exchange_select_callback, pattern="^exchange_select_.*")],
            EXCHANGE_CONFIRM: [CallbackQueryHandler(exchange_confirm_bulk_callback, pattern="^exchange_confirm_bulk_.*")],
        },
        fallbacks=[CallbackQueryHandler(showcard_callback, pattern="^showcard_")],
    )
    # --- Сначала inventory_group и album, потом menu_callback, остальные как были ---
    app.add_handler(addcard_conv)
    app.add_handler(auction_conv)
    app.add_handler(promo_conv)
    app.add_handler(addpromo_conv)
    app.add_handler(exchange_conv)
    app.add_handler(CallbackQueryHandler(inventory_group_callback, pattern="^invgroup_"))
    app.add_handler(CallbackQueryHandler(inventory_album_callback, pattern="^invalbum_"))
    app.add_handler(CallbackQueryHandler(showcard_callback, pattern="^showcard_"))
    app.add_handler(CallbackQueryHandler(buyauction_callback, pattern="^buyauction_"))
    app.add_handler(CallbackQueryHandler(showcard_refresh_callback, pattern="^showcard_refresh_"))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, group_message_handler))
    app.run_polling()

if __name__ == "__main__":
    main() 