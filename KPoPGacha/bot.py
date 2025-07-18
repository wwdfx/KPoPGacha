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

pb = PBClient()

# Шансы выпадения по редкости (сумма = 100)
RARITY_CHANCES = [
    (1, 40),   # 1 звезда - 29%
    (2, 32),   # 2 звезды - 30%
    (3, 20),   # 3 звезды - 25%
    (4, 5),   # 4 звезды - 12%
    (5, 2),    # 5 звёзд - 3%
    (6, 1),    # 6 звёзд - 1%
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

def get_reply_target(update):
    if hasattr(update, 'message') and update.message:
        return update.message
    elif hasattr(update, 'callback_query') and update.callback_query and update.callback_query.message:
        return update.callback_query.message
    return None

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
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML")
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
        await target.reply_text(text, parse_mode="HTML")

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

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML")
        return
    user_id = pb_user["id"]
    cards = pb.get_user_inventory(user_id)
    if not cards:
        if target:
            await target.reply_text("Ваша коллекция пуста!", parse_mode="HTML")
        return
    # Выводим карточки как кнопки
    keyboard = []
    for c in cards:
        card = c.get("expand", {}).get("card_id", {})
        if not card:
            continue
        btn_text = f"{card.get('name', '???')} ({card.get('group', '-')}) — {card.get('rarity', '?')}★ ×{c.get('count', 1)}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"showcard_{card.get('id')}")])
    if target:
        await target.reply_text("<b>🎴 Ваша коллекция:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

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
    # Проверяем, есть ли карточка у пользователя (count > 0)
    user_cards = pb.get_user_inventory(pb.get_user_by_telegram_id(user_id)["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    can_auction = user_card and user_card.get("count", 0) > 0
    text = (
        f"<b>{card.get('name')}</b>\n"
        f"Группа: <b>{card.get('group')}</b>\n"
        f"Альбом: <b>{card.get('album', '-')}</b>\n"
        f"Редкость: <b>{card.get('rarity')}★</b>"
    )
    keyboard = []
    if can_auction:
        keyboard.append([InlineKeyboardButton("💸 Выложить на аукцион", callback_data=f"auction_{card_id}")])
    overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
    if overlayed_path:
        with open(overlayed_path, "rb") as img_file:
            await query.message.reply_photo(img_file, caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)
        os.unlink(overlayed_path)
    elif card.get("image_url"):
        await query.message.reply_photo(card.get("image_url"), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)
    else:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

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
    await update.message.reply_text("На сколько часов выставить аукцион? (12, 24 или 48)")
    return AUCTION_DURATION

async def auction_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        hours = int(update.message.text.strip())
        if hours not in (12, 24, 48):
            raise ValueError
    except ValueError:
        await update.message.reply_text("Только 12, 24 или 48!")
        return AUCTION_DURATION
    auction_data[user_id]["duration"] = hours
    card_id = auction_data[user_id]["card_id"]
    card = pb.get_auction(card_id) if hasattr(pb, 'get_auction') else None
    text = f"Выставить карточку на аукцион за {auction_data[user_id]['price']} звёзд на {hours} ч?"
    keyboard = [[InlineKeyboardButton("✅ Да", callback_data="auction_yes"), InlineKeyboardButton("❌ Нет", callback_data="auction_no")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return AUCTION_CONFIRM

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
    auction_data.pop(user_id, None)
    return ConversationHandler.END

async def auctions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    auctions = pb.get_active_auctions()
    if not auctions:
        await update.message.reply_text("Нет активных лотов.")
        return
    keyboard = []
    for lot in auctions:
        card = lot.get("expand", {}).get("card_id", {})
        seller = lot.get("expand", {}).get("seller_id", {})
        btn_text = f"{card.get('name', '???')} ({card.get('group', '-')}) — {card.get('rarity', '?')}★ за {lot.get('price')}⭐ от {seller.get('name', '-')[:12]}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"buyauction_{lot['id']}")])
    await update.message.reply_text("<b>Аукцион:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

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
    pb.add_card_to_user(pb_buyer["id"], card["id"])
    pb.finish_auction(lot_id, status="sold", winner_id=pb_buyer["id"])
    await query.edit_message_text(f"✅ Покупка успешна! Карточка {card.get('name')} теперь ваша.")

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML")
        return
    available, last_dt = pb.check_daily_available(pb_user)
    if not available:
        if target:
            await target.reply_text("<b>Вы уже получали ежедневную награду сегодня! Возвращайтесь завтра.</b>", parse_mode="HTML")
        return
    user_id = pb_user["id"]
    stars = pb_user.get("stars", 0)
    updated_user, reward = pb.give_daily_reward(user_id, stars)
    if target:
        await target.reply_text(f"<b>🎁 Вы получили {reward} звёзд за ежедневный вход!</b>\nДо встречи завтра ✨", parse_mode="HTML")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML")
        return
    user_id = pb_user["id"]
    pulls = pb.get_pull_history(user_id, limit=10)
    if not pulls:
        if target:
            await target.reply_text("История пуста.", parse_mode="HTML")
        return
    lines = ["<b>🕓 Последние попытки:</b>"]
    for p in pulls:
        card = p.get("expand", {}).get("card_id", {})
        if not card:
            continue
        lines.append(f"<b>{card.get('name', '???')}</b> (<i>{card.get('group', '-')}</i>) — <b>{card.get('rarity', '?')}★</b> [<i>{p.get('pull_type', '')}</i>]")
    if target:
        await target.reply_text("\n".join(lines), parse_mode="HTML")

async def pity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML")
        return
    user_id = pb_user["id"]
    pity_legendary, pity_void = pb.get_pity_status(user_id)
    if target:
        await target.reply_text(f"<b>🎯 Pity Legendary:</b> {pity_legendary}/80\n<b>🕳️ Pity Void:</b> {pity_void}/165", parse_mode="HTML")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    top = pb.get_leaderboard(limit=10)
    if not top:
        if target:
            await target.reply_text("Лидерборд пуст.", parse_mode="HTML")
        return
    lines = ["<b>🏆 Топ коллекционеров:</b>"]
    for i, user in enumerate(top, 1):
        name = user.get("name") or f"User {user.get('telegram_id', '')}" 
        level = user.get("level", 1)
        exp = user.get("exp", 0)
        rank = pb.get_rank(level)
        lines.append(f"{i}. <b>{name}</b> — <b>{level}</b> <i>({rank})</i>, опыт: <b>{exp}</b>")
    if target:
        await target.reply_text("\n".join(lines), parse_mode="HTML")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = get_reply_target(update)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML")
        return
    if target:
        await target.reply_text("<b>⚙️ Настройки профиля будут доступны в будущих обновлениях.</b>", parse_mode="HTML")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Профиль", callback_data="profile"), InlineKeyboardButton("🎴 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton("🎲 Гача (1)", callback_data="pull"), InlineKeyboardButton("🔟 Гача (10)", callback_data="pull10")],
        [InlineKeyboardButton("🎁 Ежедневка", callback_data="daily"), InlineKeyboardButton("🕓 История", callback_data="history")],
        [InlineKeyboardButton("🎯 Pity", callback_data="pity"), InlineKeyboardButton("🏆 Лидерборд", callback_data="leaderboard")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = get_reply_target(update)
    if target:
        await target.reply_text("<b>Главное меню:</b>", reply_markup=reply_markup, parse_mode="HTML")

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    # Просто вызываем нужную функцию
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
            AUCTION_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, auction_duration)],
            AUCTION_CONFIRM: [CallbackQueryHandler(auction_confirm, pattern="^auction_(yes|no)$")],
        },
        fallbacks=[CommandHandler("cancel", addcard_cancel)],
    )
    app.add_handler(auction_conv)
    app.add_handler(CallbackQueryHandler(showcard_callback, pattern="^showcard_"))
    app.add_handler(CallbackQueryHandler(buyauction_callback, pattern="^buyauction_"))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, group_message_handler))
    app.run_polling()

if __name__ == "__main__":
    main() 