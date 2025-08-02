from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from pb_client import PBClient
from config import TELEGRAM_BOT_TOKEN, ADMIN_IDS, TELEGRAM_AUCTION_CHANNEL_ID
import random
import os
import tempfile
import requests
from PIL import Image
from telegram.ext import ConversationHandler, MessageHandler, filters
from collections import defaultdict
import httpx
import asyncio
from telegram.constants import ParseMode, ChatType
import uuid

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

BANNER_GROUP, BANNER_ALBUM, BANNER_CONFIRM = range(50, 53)

TRADE_SELECT_USER, TRADE_SELECT_OTHER_CARD, TRADE_CONFIRM = range(60, 63)
trade_data = {}

TRADE_PAGE_SIZE = 10

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

async def drop100(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Только для администратора.")
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Использование: /drop100 <user_id>")
        return
    target_tg_id = int(context.args[0])
    pb_user = pb.get_user_by_telegram_id(target_tg_id)
    if not pb_user:
        await update.message.reply_text(f"Пользователь с Telegram ID {target_tg_id} не найден.")
        return
    all_cards = pb.get_all_cards()
    if not all_cards:
        await update.message.reply_text("В базе нет карточек.")
        return
    import random
    dropped = random.choices(all_cards, k=100)
    for card in dropped:
        pb.add_card_to_user(pb_user["id"], card["id"])
    await update.message.reply_text(f"✅ Выдано 100 случайных карточек пользователю {pb_user.get('name', target_tg_id)} (ID: {target_tg_id})!")

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
    user = update.effective_user
    args = context.args
    if args and args[0].startswith("bonus_"):
        from config import DAILY_BONUS_REWARD
        try:
            _, tg_id, token = args[0].split("_", 2)
        except Exception:
            await update.message.reply_text("Некорректная бонус-ссылка.")
            return
        pb_user = pb.get_user_by_telegram_id(tg_id)
        if not pb_user:
            await update.message.reply_text("Пользователь не найден.")
            return
        ok = pb.check_and_consume_daily_bonus(pb_user["id"], token)
        if ok:
            new_stars = pb_user.get("stars", 0) + DAILY_BONUS_REWARD
            pb.update_user_stars_and_pity(pb_user["id"], new_stars, pb_user.get("pity_legendary", 0), pb_user.get("pity_void", 0))
            await update.message.reply_text(f"🎁 Вы получили {DAILY_BONUS_REWARD} звёзд за ежедневный бонус!")
        else:
            await update.message.reply_text("Бонус уже получен или ссылка неактивна.")
        return
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
    group, album = pb.get_active_banner(pb_user)
    if group and album:
        banner_str = f"<b>Баннер:</b> <i>{group} — {album}</i>"
    else:
        banner_str = "<b>Баннер:</b> <i>Общий (все карты)</i>"
    text = (
        f"<b>👤 Профиль:</b>\n"
        f"<b>Имя:</b> {pb_user.get('name', '')}\n"
        f"<b>Уровень:</b> {pb_user.get('level', 1)} <i>({rank})</i>\n"
        f"<b>Опыт:</b> {pb_user.get('exp', 0)} / {pb.exp_to_next_level(pb_user.get('level', 1))}\n"
        f"<b>⭐ Звёзды:</b> {pb_user.get('stars', 0)}\n"
        f"<b>🎯 Pity Legendary:</b> {pb_user.get('pity_legendary', 0)} / 80\n"
        f"<b>🕳️ Pity Void:</b> {pb_user.get('pity_void', 0)} / 165\n"
        f"{banner_str}"
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
    # --- Баннер ---
    group, album = pb.get_active_banner(pb_user)
    if group and album:
        all_cards = pb.get_cards_by_group_album(group, album)
        cards_of_rarity = [c for c in all_cards if c.get("rarity") == rarity]
        card = random.choice(cards_of_rarity) if cards_of_rarity else None
    else:
        card = pb.get_random_card_by_rarity(rarity)
    if not card:
        if target:
            await target.reply_text(f"Нет карточек с редкостью {rarity}★ в выбранном баннере!", parse_mode="HTML")
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
    banner_text = f"<b>Баннер:</b> <i>{group} — {album}</i>\n" if group and album else ""
    text = (
        f"{banner_text}<b>Выпала карта:</b> <b>{card['name']}</b> (<i>{card['group']}</i>)\n"
        f"<b>Редкость:</b> <b>{card['rarity']}★</b>\n<b>+{base_exp} опыта</b>"
    )
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
    group, album = pb.get_active_banner(pb_user)
    results = []
    media = []
    captions = []
    total_exp = 0
    rolls = 0
    max_rolls = 200  # Увеличиваем лимит попыток
    banner_text = f"<b>Баннер:</b> <i>{group} — {album}</i>\n" if group and album else ""
    
    # Кэшируем карты баннера один раз
    banner_cards = None
    if group and album:
        banner_cards = pb.get_cards_by_group_album(group, album)
    
    while len(results) < 10 and rolls < max_rolls:
        rarity = choose_rarity(pity_legendary, pity_void)
        if group and album and banner_cards:
            cards_of_rarity = [c for c in banner_cards if c.get("rarity") == rarity]
            if not cards_of_rarity:
                # Если нет карт нужной редкости, берем любую доступную
                card = random.choice(banner_cards)
            else:
                card = random.choice(cards_of_rarity)
        else:
            card = pb.get_random_card_by_rarity(rarity)
            if not card:
                rolls += 1
                continue
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
        pb.add_card_to_user(user_id, card["id"])
        pb.add_pull_history(user_id, card["id"], "multi")
        base_exp = PBClient.RARITY_EXP.get(card["rarity"], 1)
        is_first = pb.is_first_card(user_id, card["id"])
        exp_gain = base_exp + (base_exp // 2 if is_first else 0)
        total_exp += exp_gain
        caption = (
            f"{banner_text}<b>{card['name']}</b> (<i>{card['group']}</i>)\n"
            f"Альбом: <b>{card.get('album', '-') if card.get('album') else '-'}</b>\n"
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
            results.append(f"{len(results)+1}. {card['name']} — нет изображения")
        results.append(card)
        rolls += 1
    if len(results) < 10:
        await target.reply_text(f"Не удалось получить 10 карточек после {max_rolls} попыток. Возможно, в баннере недостаточно карточек разных редкостей.", parse_mode="HTML")
        return
    pb.update_user_stars_and_pity(user_id, stars - PULL10_COST, pity_legendary, pity_void)
    updated_user, levelup = pb.add_exp_and_check_levelup(user_id, level, exp, total_exp)
    if media:
        # Если карт много, отправляем текстовое резюме
        if len(media) > 5:
            summary = f"{banner_text}<b>🎉 Получено {len(media)} карточек!</b>\n\n"
            rarity_summary = {}
            for m in media:
                # Извлекаем редкость из caption
                caption = m.caption
                if "Редкость: " in caption:
                    rarity_line = caption.split("Редкость: ")[1].split(" ")[0]
                    # Убираем HTML-теги и символы
                    rarity_clean = rarity_line.replace("★", "").replace("<b>", "").replace("</b>", "")
                    rarity = int(rarity_clean)
                    rarity_summary[rarity] = rarity_summary.get(rarity, 0) + 1
            
            for rarity in sorted(rarity_summary.keys()):
                summary += f"<b>{rarity}★</b>: {rarity_summary[rarity]} карт\n"
            
            await target.reply_text(summary, parse_mode="HTML")
        else:
            try:
                await target.reply_media_group(media)
            except Exception as e:
                print(f"DEBUG: Ошибка отправки медиа-группы: {e}")
                # Отправляем по одной карте с задержкой
                for i, m in enumerate(media):
                    try:
                        await target.reply_photo(m.media, caption=m.caption, parse_mode="HTML")
                        if i < len(media) - 1:  # Не делаем задержку после последней карты
                            await asyncio.sleep(1.0)  # Увеличиваем задержку между отправками
                    except Exception as e:
                        print(f"DEBUG: Ошибка отправки карты {i+1}: {e}")
                        # Если не удалось отправить фото, отправляем текстом
                        await target.reply_text(m.caption, parse_mode="HTML")
        for path in captions:
            if path:
                try:
                    os.unlink(path)
                except Exception:
                    pass
    if levelup:
        rank = pb.get_rank(updated_user.get('level', 1))
        await target.reply_text(f"\n<b>Поздравляем! Ваш уровень повышен: {updated_user.get('level', 1)} ({rank})</b>", parse_mode="HTML")

# --- Новый инвентарь: группировка по группам и альбомам ---
async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prefer_edit = hasattr(update, 'callback_query') and update.callback_query is not None
    target = get_reply_target(update, prefer_edit=prefer_edit)
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        if target:
            if prefer_edit:
                try:
                    await target.edit_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
                except Exception:
                    await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
            else:
                await target.reply_text("Профиль не найден. Используйте /start.", parse_mode="HTML", reply_markup=back_keyboard())
        return
    user_id = pb_user["id"]
    cards = pb.get_user_inventory(user_id)
    if not cards:
        if target:
            if prefer_edit:
                try:
                    await target.edit_text("Ваша коллекция пуста!", parse_mode="HTML", reply_markup=back_keyboard())
                except Exception:
                    await target.reply_text("Ваша коллекция пуста!", parse_mode="HTML", reply_markup=back_keyboard())
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
            try:
                await target.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            except Exception:
                await target.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
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
        if card.get("group", "-").strip().lower() == group.strip().lower():
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
    from config import ACHIEVEMENT_REWARDS
    query = update.callback_query
    if query.data == "none":
        await query.answer("У вас нет этой карточки!", show_alert=True)
        return
    await query.answer()
    data = query.data.replace("invalbum_", "")
    group, album = data.split("__", 1)
    user_id = query.from_user.id
    pb_user = pb.get_user_by_telegram_id(user_id)
    user_cards = pb.get_user_inventory(pb_user["id"])
    # Получаем все карточки коллекции
    all_cards = pb.get_cards_by_group_album(group, album)
    # Собираем user_card_id -> count
    user_card_map = {c.get("expand", {}).get("card_id", {}).get("id"): c.get("count", 0) for c in user_cards if c.get("expand", {}).get("card_id", {}).get("group", "-").strip().lower() == group.strip().lower() and c.get("expand", {}).get("card_id", {}).get("album", "-").strip().lower() == album.strip().lower()}
    # Сортируем по убыванию редкости, затем по имени
    all_cards.sort(key=lambda c: (-c.get("rarity", 1), c.get("name", "")))
    have = 0
    card_buttons = []
    for card in all_cards:
        cid = card.get("id")
        count = user_card_map.get(cid, 0)
        if count > 0:
            btn_text = f"✅ {card.get('name', '???')} — {card.get('rarity', '?')}★ ×{count}"
            card_buttons.append([InlineKeyboardButton(btn_text, callback_data=f"showcard_{cid}")])
            have += 1
        else:
            btn_text = f"❌ {card.get('name', '???')} — {card.get('rarity', '?')}★"
            card_buttons.append([InlineKeyboardButton(btn_text, callback_data="none")])
    card_buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data=f"invgroup_{group}")])
    percent = int(have / max(1, len(all_cards)) * 100)
    text = f"<b>Группа:</b> <b>{group}</b>\n<b>Альбом:</b> <b>{album}</b>\n\n<b>Собрано:</b> <b>{have} / {len(all_cards)}</b> (<b>{percent}%</b>)\n\n<code>✅ — есть  ❌ — нет</code>\nВыберите карточку:"
    # --- Ачивки за прогресс ---
    ach_level = 0
    if percent >= 100:
        ach_level = 4
    elif percent >= 75:
        ach_level = 3
    elif percent >= 50:
        ach_level = 2
    elif percent >= 25:
        ach_level = 1
    if ach_level > 0:
        ach = pb.get_collection_achievement(pb_user["id"], group, album)
        prev_level = ach["level"] if ach else 0
        if ach_level > prev_level:
            # Выдаём награду
            reward = ACHIEVEMENT_REWARDS.get(ach_level, {"exp": 0, "stars": 0})
            pb.set_collection_achievement(pb_user["id"], group, album, ach_level)
            # Обновляем опыт и звёзды
            new_exp = pb_user.get("exp", 0) + reward["exp"]
            new_stars = pb_user.get("stars", 0) + reward["stars"]
            pb.update_user_stars_and_pity(pb_user["id"], new_stars, pb_user.get("pity_legendary", 0), pb_user.get("pity_void", 0))
            pb.add_exp_and_check_levelup(pb_user["id"], pb_user.get("level", 1), pb_user.get("exp", 0), reward["exp"])
            try:
                await query.message.reply_text(f"🏆 <b>Ачивка!</b> За {ach_level*25}% коллекции альбома <b>{album}</b> вы получили <b>{reward['exp']} опыта</b> и <b>{reward['stars']} звёзд</b>!", parse_mode="HTML")
            except Exception:
                pass
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
        try:
            if query.message and query.message.photo:
                await query.message.edit_caption("Карточка не найдена.")
            else:
                await query.edit_message_text("Карточка не найдена.")
        except Exception:
            await query.message.reply_text("Карточка не найдена.")
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
    # Кнопка обмена
    if count > 0:
        keyboard.append([InlineKeyboardButton("🔄 Обменяться", callback_data=f"trade_start_{card_id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="inventory")])
    overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
    if overlayed_path:
        with open(overlayed_path, "rb") as img_file:
            await query.message.reply_photo(img_file, caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        os.unlink(overlayed_path)
    elif card.get("image_url"):
        await query.message.reply_photo(card.get("image_url"), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        try:
            if query.message and query.message.photo:
                await query.message.edit_caption(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
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
    # --- Отправка сообщения в канал ---
    # Получаем карточку
    url = f"{pb.base_url}/collections/cards/records/{data['card_id']}"
    resp = requests.get(url, headers=pb.headers)
    card = resp.json() if resp.status_code == 200 else {}
    overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
    seller_name = pb_user.get("name", "?")
    text = (
        f"<b>🛒 Новый лот на аукционе!</b>\n"
        f"<b>{card.get('name', '???')}</b>\n"
        f"Группа: <b>{card.get('group', '-')}</b>\n"
        f"Альбом: <b>{card.get('album', '-')}</b>\n"
        f"Редкость: <b>{card.get('rarity', '?')}★</b>\n"
        f"Цена: <b>{data['price']}⭐</b>\n"
        f"Срок: <b>{data['duration']} ч.</b>\n"
        f"Продавец: <b>{seller_name}</b>"
    )
    try:
        if overlayed_path:
            with open(overlayed_path, "rb") as img_file:
                await context.bot.send_photo(
                    chat_id=TELEGRAM_AUCTION_CHANNEL_ID,
                    photo=img_file,
                    caption=text,
                    parse_mode="HTML"
                )
            os.unlink(overlayed_path)
        elif card.get("image_url"):
            await context.bot.send_photo(
                chat_id=TELEGRAM_AUCTION_CHANNEL_ID,
                photo=card.get("image_url"),
                caption=text,
                parse_mode="HTML"
            )
        else:
            await context.bot.send_message(
                chat_id=TELEGRAM_AUCTION_CHANNEL_ID,
                text=text,
                parse_mode="HTML"
            )
    except Exception as e:
        print(f"[AUCTION CHANNEL ERROR] {e}")
    await query.edit_message_text("✅ Карточка выставлена на аукцион!")
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
    user = update.effective_user if hasattr(update, 'effective_user') else None
    pb_user = pb.get_user_by_telegram_id(user.id) if user else None
    group, album = pb.get_active_banner(pb_user) if pb_user else (None, None)
    if group and album:
        banner_str = f"<b>Баннер:</b> <i>{group} — {album}</i>"
    else:
        banner_str = "<b>Баннер:</b> <i>Общий (все карты)</i>"
    keyboard = [
        [InlineKeyboardButton("👤 Профиль", callback_data="profile"), InlineKeyboardButton("🎴 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton("🎲 Гача (1)", callback_data="pull"), InlineKeyboardButton("🔟 Гача (10)", callback_data="pull10")],
        [InlineKeyboardButton("🎁 Ежедневка", callback_data="daily"), InlineKeyboardButton("🕓 История", callback_data="history")],
        [InlineKeyboardButton("🎯 Pity", callback_data="pity"), InlineKeyboardButton("🏆 Лидерборд", callback_data="leaderboard")],
        [InlineKeyboardButton("🛒 Аукцион", callback_data="auctions")],
        [InlineKeyboardButton("🏅 Достижения", callback_data="achievements")],
        [InlineKeyboardButton("🎤 Баннер", callback_data="banner")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = get_reply_target(update, prefer_edit=prefer_edit)
    menu_text = f"<b>Главное меню:</b>\n{banner_str}"
    if target:
        if prefer_edit:
            await target.edit_text(menu_text, reply_markup=reply_markup, parse_mode="HTML")
        else:
            await target.reply_text(menu_text, reply_markup=reply_markup, parse_mode="HTML")

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print(f"[menu_callback] query.data: {query.data}")
    data = query.data
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
    elif data == "achievements":
        await achievements(update, context)
    elif data == "banner":
        await banner_start(update, context)
    else:
        try:
            await query.edit_message_text("Неизвестная команда.")
        except Exception:
            await query.message.reply_text("Неизвестная команда.")

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
    print(f"[exchange_confirm_bulk_callback] card_id:", card_id)
    user_id = query.from_user.id
    user = pb.get_user_by_telegram_id(user_id)
    user_cards = pb.get_user_inventory(user["id"])
    user_card = next((c for c in user_cards if c.get("card_id") == card_id or (c.get("expand", {}).get("card_id", {}).get("id") == card_id)), None)
    print(f"[exchange_confirm_bulk_callback] user_card:", user_card)
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
    query = update.callback_query
    await query.answer()
    card_id = query.data.replace("showcard_refresh_", "")
    print(f"[showcard_refresh_callback] card_id:", card_id)
    url = f"{pb.base_url}/collections/cards/records/{card_id}"
    resp = requests.get(url, headers=pb.headers)
    print(f"[showcard_refresh_callback] resp.status_code:", resp.status_code)
    if resp.status_code != 200:
        # Возвращаем пользователя в инвентарь вместо ошибки
        await inventory(update, context)
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
    # Кнопка обмена
    if count > 0:
        keyboard.append([InlineKeyboardButton("🔄 Обменяться", callback_data=f"trade_start_{card_id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="inventory")])
    overlayed_path = apply_overlay(card.get("image_url"), card.get("rarity"))
    # Если сообщение было фото, удаляем его и отправляем новое
    if query.message and query.message.photo:
        try:
            await query.message.delete()
        except Exception:
            pass
        if overlayed_path:
            with open(overlayed_path, "rb") as img_file:
                await query.message.reply_photo(img_file, caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
            os.unlink(overlayed_path)
        elif card.get("image_url"):
            await query.message.reply_photo(card.get("image_url"), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        if overlayed_path:
            with open(overlayed_path, "rb") as img_file:
                await query.message.reply_photo(img_file, caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
            os.unlink(overlayed_path)
        elif card.get("image_url"):
            await query.message.reply_photo(card.get("image_url"), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    target = get_reply_target(update, prefer_edit=hasattr(update, 'callback_query') and update.callback_query is not None)
    if not pb_user:
        await target.reply_text("Профиль не найден. Используйте /start.")
        return
    achs = []
    # Получаем все достижения пользователя
    url = f"{pb.base_url}/collections/collection_achievements/records"
    params = {"filter": f'user_id="{pb_user["id"]}"', "perPage": 200}
    import httpx
    resp = httpx.get(url, headers=pb.headers, params=params)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        await target.reply_text("У вас пока нет достижений по коллекциям.")
        return
    # Группируем по группе и альбому
    items.sort(key=lambda x: (x.get("group", ""), x.get("album", "")))
    text = "<b>🏅 Ваши достижения по коллекциям:</b>\n"
    for ach in items:
        group = ach.get("group", "-")
        album = ach.get("album", "-")
        level = ach.get("level", 0)
        if level > 0:
            text += f"\n<b>{group}</b> — <b>{album}</b>: <b>{level*25}%</b>"
    if hasattr(target, 'edit_text'):
        await target.edit_text(text, parse_mode="HTML")
    else:
        await target.reply_text(text, parse_mode="HTML")

async def send_daily_bonus_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Только для администратора.")
        return
    import uuid
    pb = PBClient()
    bot = context.bot
    bot_username = 'kpop_gacha_bot'  # или получи через await bot.get_me()
    users = pb.get_all_users()
    count = 0
    for user in users:
        user_id = user["id"]
        tg_id = user["telegram_id"]
        token = str(uuid.uuid4())
        pb.set_daily_bonus_token(user_id, token)
        link = f"https://t.me/{bot_username}?start=bonus_{tg_id}_{token}"
        try:
            await bot.send_message(
                chat_id=int(tg_id),
                text=f"🌟 Ваш ежедневный бонус! Жмите на кнопку ниже, чтобы получить 25 звёзд!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Получить бонус', url=link)]]),
                parse_mode=ParseMode.HTML
            )
            count += 1
        except Exception as e:
            print(f"Не удалось отправить бонус пользователю {tg_id}: {e}")
    await update.message.reply_text(f"✅ Бонусные ссылки отправлены {count} пользователям.")

async def banner_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        target = get_reply_target(update, prefer_edit=True)
        await target.reply_text("Профиль не найден. Используйте /start.")
        return ConversationHandler.END
    # Получаем все уникальные группы
    all_cards = pb.get_all_cards()
    group_set = set(c.get("group", "-") for c in all_cards if c.get("group"))
    keyboard = [[InlineKeyboardButton(g, callback_data=f"banner_group_{g}")] for g in sorted(group_set)]
    keyboard.append([InlineKeyboardButton("🌐 Общий баннер (все карты)", callback_data="banner_reset")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="menu")])
    target = get_reply_target(update, prefer_edit=True)
    await target.reply_text("<b>Выберите группу для баннера:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return BANNER_GROUP

async def banner_group_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group = query.data.replace("banner_group_", "")
    all_cards = pb.get_all_cards()
    group_norm = group.strip().lower()
    print(f"DEBUG: Все карточки группы {group}")
    for c in all_cards:
        if c.get("group") and c.get("group").strip().lower() == group_norm:
            print("  Альбом:", repr(c.get("album")))
    album_set = set(
        c.get("album", "-")
        for c in all_cards
        if c.get("group") and c.get("group").strip().lower() == group_norm and c.get("album")
    )
    keyboard = [[InlineKeyboardButton(a, callback_data=f"banner_album_{group}__{a}")] for a in sorted(album_set)]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="banner")])
    await query.edit_message_text(f"<b>Группа:</b> <b>{group}</b>\nВыберите альбом:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return BANNER_ALBUM

async def banner_album_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.replace("banner_album_", "")
    group, album = data.split("__", 1)
    context.user_data["banner"] = {"group": group, "album": album}
    keyboard = [
        [InlineKeyboardButton(f"✅ Крутить только {album} ({group})", callback_data="banner_confirm")],
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"banner_group_{group}")]
    ]
    await query.edit_message_text(f"Вы выбрали баннер: <b>{group}</b> — <b>{album}</b>\nПодтвердите выбор:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return BANNER_CONFIRM

async def banner_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    banner = context.user_data.get("banner")
    if not banner:
        await query.edit_message_text("Ошибка выбора баннера.")
        return ConversationHandler.END
    pb.set_active_banner(pb_user["id"], banner["group"], banner["album"])
    await query.edit_message_text(f"✅ Теперь ваши пуллы будут только по альбому <b>{banner['album']}</b> группы <b>{banner['group']}</b>!", parse_mode="HTML", reply_markup=back_keyboard())
    return ConversationHandler.END

async def banner_reset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    pb.reset_active_banner(pb_user["id"])
    await query.edit_message_text("🌐 Баннер сброшен. Теперь пуллы идут по всем картам!", parse_mode="HTML", reply_markup=back_keyboard())
    return ConversationHandler.END

async def trade_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    card_id = query.data.replace("trade_start_", "")
    context.user_data["trade"] = {"my_card_id": card_id}
    text = (
        "<b>Обмен карточками</b>\n"
        "С кем вы хотите обменяться?\n"
        "<i>Ответьте на сообщение пользователя, с которым хотите обменяться, или введите его username/id в чат.</i>"
    )
    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="trade_cancel")]]
    try:
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception:
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    return TRADE_SELECT_USER

async def trade_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text("Обмен отменён.")
    except Exception:
        await query.message.reply_text("Обмен отменён.")
    context.user_data.pop("trade", None)
    return ConversationHandler.END

async def trade_user_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    trade = context.user_data.get("trade", {})
    if update.message.reply_to_message:
        other_user = update.message.reply_to_message.from_user
    else:
        text = update.message.text.strip()
        other_user = None
        if text.startswith("@"):  # username
            try:
                other_user = await context.bot.get_chat(text)
            except Exception:
                pass
        elif text.isdigit():  # id
            try:
                other_user = await context.bot.get_chat(int(text))
            except Exception:
                pass
    if not other_user or other_user.id == user.id:
        await update.message.reply_text("Пользователь не найден или выбран некорректно. Попробуйте ещё раз.")
        return TRADE_SELECT_USER
    trade["other_user_id"] = other_user.id
    context.user_data["trade"] = trade
    pb_other = pb.get_user_by_telegram_id(other_user.id)
    if not pb_other:
        await update.message.reply_text("У выбранного пользователя нет профиля в боте.")
        return TRADE_SELECT_USER
    other_cards = pb.get_user_inventory(pb_other["id"])
    # Фильтруем только те, у которых count > 0
    card_list = [c for c in other_cards if c.get("expand", {}).get("card_id", {}) and c.get("count", 0) > 0]
    if not card_list:
        await update.message.reply_text("У выбранного пользователя нет карточек для обмена.")
        return ConversationHandler.END
    # Сохраняем список карточек и текущую страницу в context.user_data
    context.user_data["trade_other_cards"] = card_list
    context.user_data["trade_page"] = 0
    await show_trade_page(update, context, other_user, 0)
    return TRADE_SELECT_OTHER_CARD

async def show_trade_page(update, context, other_user, page):
    card_list = context.user_data.get("trade_other_cards", [])
    total = len(card_list)
    start = page * TRADE_PAGE_SIZE
    end = start + TRADE_PAGE_SIZE
    page_cards = card_list[start:end]
    card_buttons = []
    for c in page_cards:
        card = c.get("expand", {}).get("card_id", {})
        btn_text = f"{card.get('name', '???')} — {card.get('rarity', '?')}★"
        card_buttons.append([InlineKeyboardButton(btn_text, callback_data=f"trade_select_other_{card.get('id')}")])
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⏪ Назад", callback_data="trade_page_prev"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton("⏩ Далее", callback_data="trade_page_next"))
    if nav_buttons:
        card_buttons.append(nav_buttons)
    card_buttons.append([InlineKeyboardButton("❌ Отмена", callback_data="trade_cancel")])
    text = f"Выберите, какую карточку хотите получить у @{other_user.username or other_user.id} (стр. {page+1}/{(total-1)//TRADE_PAGE_SIZE+1}):"
    # Если это первый вызов (после выбора пользователя) — reply, иначе edit
    if hasattr(update, "message") and update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(card_buttons))
    else:
        try:
            await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(card_buttons))
        except Exception:
            await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(card_buttons))

async def trade_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = context.user_data.get("trade_page", 0)
    if query.data == "trade_page_next":
        page += 1
    elif query.data == "trade_page_prev":
        page = max(0, page - 1)
    context.user_data["trade_page"] = page
    trade = context.user_data.get("trade", {})
    other_user_id = trade.get("other_user_id")
    if not other_user_id:
        await query.edit_message_text("Ошибка: не выбран пользователь для обмена.")
        return ConversationHandler.END
    other_user = await context.bot.get_chat(other_user_id)
    await show_trade_page(update, context, other_user, page)
    return TRADE_SELECT_OTHER_CARD

async def trade_select_other_card_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = query.data.replace("trade_select_other_", "")
    trade = context.user_data.get("trade", {})
    trade["other_card_id"] = card_id
    context.user_data["trade"] = trade
    user = update.effective_user
    other_user_id = trade["other_user_id"]
    pb_other = pb.get_user_by_telegram_id(other_user_id)
    pb_user = pb.get_user_by_telegram_id(user.id)
    my_card = None
    other_card = None
    my_cards = pb.get_user_inventory(pb_user["id"])
    for c in my_cards:
        card = c.get("expand", {}).get("card_id", {})
        if card.get("id") == trade["my_card_id"]:
            my_card = card
            break
    other_cards = pb.get_user_inventory(pb_other["id"])
    for c in other_cards:
        card = c.get("expand", {}).get("card_id", {})
        if card.get("id") == trade["other_card_id"]:
            other_card = card
            break
    if not my_card or not other_card:
        try:
            await query.edit_message_text("Ошибка: не удалось найти выбранные карточки.")
        except Exception:
            await query.message.reply_text("Ошибка: не удалось найти выбранные карточки.")
        return ConversationHandler.END
    trade_data[other_user_id] = {
        "from_user_id": user.id,
        "my_card_id": trade["my_card_id"],
        "other_card_id": trade["other_card_id"]
    }
    text = (
        f"<b>Вам предлагают обмен!</b>\n"
        f"Пользователь <b>{user.full_name}</b> предлагает обменяться:\n"
        f"Отдаёт: <b>{other_card.get('name', '?')}</b> ({other_card.get('rarity', '?')}★)\n"
        f"Взамен хочет: <b>{my_card.get('name', '?')}</b> ({my_card.get('rarity', '?')}★)\n"
        f"Принять обмен?"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Принять", callback_data="trade_accept"), InlineKeyboardButton("❌ Отклонить", callback_data="trade_decline")]
    ]
    try:
        await context.bot.send_message(chat_id=other_user_id, text=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
        await query.edit_message_text("Запрос на обмен отправлен! Ожидаем подтверждения.")
    except Exception as e:
        try:
            await query.edit_message_text(f"Не удалось отправить запрос: {e}")
        except Exception:
            await query.message.reply_text(f"Не удалось отправить запрос: {e}")
    return ConversationHandler.END

async def trade_accept_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    trade = trade_data.pop(user_id, None)
    if not trade:
        await query.edit_message_text("Запрос на обмен не найден или устарел.")
        return ConversationHandler.END
    # Проверяем, что у обоих есть нужные карточки
    pb_user = pb.get_user_by_telegram_id(trade["from_user_id"])
    pb_other = pb.get_user_by_telegram_id(user_id)
    my_cards = pb.get_user_inventory(pb_user["id"])
    other_cards = pb.get_user_inventory(pb_other["id"])
    my_card = next((c for c in my_cards if c.get("expand", {}).get("card_id", {}).get("id") == trade["my_card_id"] and c.get("count", 0) > 0), None)
    other_card = next((c for c in other_cards if c.get("expand", {}).get("card_id", {}).get("id") == trade["other_card_id"] and c.get("count", 0) > 0), None)
    print(f"[trade_accept_callback] my_card: {my_card}")
    print(f"[trade_accept_callback] other_card: {other_card}")
    if not my_card or not other_card:
        await query.edit_message_text("Одна из карточек уже отсутствует у игрока. Обмен невозможен.")
        return ConversationHandler.END
    # Совершаем обмен: уменьшаем count у обоих, добавляем карточку другому
    pb.add_card_to_user(pb_user["id"], trade["other_card_id"])
    pb.add_card_to_user(pb_other["id"], trade["my_card_id"])
    # Уменьшаем count у обоих
    url1 = f"{pb.base_url}/collections/user_cards/records/{my_card['id']}"
    url2 = f"{pb.base_url}/collections/user_cards/records/{other_card['id']}"
    print(f"[trade_accept_callback] PATCH {url1} count: {my_card['count']} -> {my_card['count']-1}")
    print(f"[trade_accept_callback] PATCH {url2} count: {other_card['count']} -> {other_card['count']-1}")
    httpx.patch(url1, headers=pb.headers, json={"count": my_card["count"] - 1})
    httpx.patch(url2, headers=pb.headers, json={"count": other_card["count"] - 1})
    # Проверяем результат
    my_cards_after = pb.get_user_inventory(pb_user["id"])
    other_cards_after = pb.get_user_inventory(pb_other["id"])
    print(f"[trade_accept_callback] my_cards_after: {[{'id':c.get('expand',{}).get('card_id',{}).get('id'), 'count':c.get('count')} for c in my_cards_after]}")
    print(f"[trade_accept_callback] other_cards_after: {[{'id':c.get('expand',{}).get('card_id',{}).get('id'), 'count':c.get('count')} for c in other_cards_after]}")
    await query.edit_message_text("Обмен успешно завершён! Карточки обменялись между игроками.")
    # Оповещаем инициатора
    try:
        await context.bot.send_message(chat_id=pb_user["telegram_id"], text="Ваш обмен успешно завершён!", parse_mode="HTML")
    except Exception:
        pass
    return ConversationHandler.END

async def trade_decline_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    trade = trade_data.pop(user_id, None)
    await query.edit_message_text("Обмен отклонён.")
    # Оповещаем инициатора
    if trade:
        try:
            pb_user = pb.get_user_by_telegram_id(trade["from_user_id"])
            await context.bot.send_message(chat_id=pb_user["telegram_id"], text="Ваш обмен был отклонён.", parse_mode="HTML")
        except Exception:
            pass
    return ConversationHandler.END

# ConversationHandler для обмена
trade_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(trade_start_callback, pattern="^trade_start_")],
    states={
        TRADE_SELECT_USER: [MessageHandler(filters.REPLY | filters.TEXT & ~filters.COMMAND, trade_user_select)],
        TRADE_SELECT_OTHER_CARD: [CallbackQueryHandler(trade_select_other_card_callback, pattern="^trade_select_other_.*"),
                                 CallbackQueryHandler(trade_page_callback, pattern="^trade_page_(next|prev)$")],
    },
    fallbacks=[CallbackQueryHandler(trade_cancel_callback, pattern="^trade_cancel")],
)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
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
    app.add_handler(trade_conv)
    app.add_handler(CallbackQueryHandler(trade_accept_callback, pattern="^trade_accept$"))
    app.add_handler(CallbackQueryHandler(trade_decline_callback, pattern="^trade_decline$"))
    app.add_handler(exchange_conv)
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
    app.add_handler(CommandHandler("drop100", drop100))
    app.add_handler(CommandHandler("achievements", achievements))
    app.add_handler(CommandHandler("senddailybonus", send_daily_bonus_links))
    app.add_handler(CommandHandler("banner", banner_start))
    app.add_handler(CallbackQueryHandler(banner_group_callback, pattern="^banner_group_"))
    app.add_handler(CallbackQueryHandler(banner_album_callback, pattern="^banner_album_"))
    app.add_handler(CallbackQueryHandler(banner_confirm_callback, pattern="^banner_confirm$"))
    app.add_handler(CallbackQueryHandler(banner_reset_callback, pattern="^banner_reset$"))
    app.add_handler(CallbackQueryHandler(inventory_group_callback, pattern="^invgroup_"))
    app.add_handler(CallbackQueryHandler(inventory_album_callback, pattern="^invalbum_"))
    app.add_handler(CallbackQueryHandler(showcard_callback, pattern="^showcard_"))
    app.add_handler(CallbackQueryHandler(buyauction_callback, pattern="^buyauction_"))
    app.add_handler(CallbackQueryHandler(showcard_refresh_callback, pattern="^showcard_refresh_"))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, group_message_handler))
    app.add_handler(addcard_conv)
    app.add_handler(auction_conv)
    app.add_handler(promo_conv)
    app.add_handler(addpromo_conv)
    app.run_polling()

if __name__ == "__main__":
    main() 