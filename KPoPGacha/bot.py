from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pb_client import PBClient
from config import TELEGRAM_BOT_TOKEN
import random

pb = PBClient()

# Шансы выпадения по редкости (сумма = 100)
RARITY_CHANCES = [
    (1, 29),   # 1 звезда - 29%
    (2, 30),   # 2 звезды - 30%
    (3, 25),   # 3 звезды - 25%
    (4, 12),   # 4 звезды - 12%
    (5, 3),    # 5 звёзд - 3%
    (6, 1),    # 6 звёзд - 1%
]
RARITY_WEIGHTS = [chance for _, chance in RARITY_CHANCES]
RARITY_VALUES = [rarity for rarity, _ in RARITY_CHANCES]

PULL_COST = 10  # Стоимость одной попытки в звёздах
PULL10_COST = 90  # Стоимость 10 попыток (скидка)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        pb.create_user(user.id, user.full_name)
        await update.message.reply_text(f"Добро пожаловать, {user.full_name}! Ваш игровой профиль создан.")
    else:
        await update.message.reply_text(f"С возвращением, {user.full_name}!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - начать\n/profile - профиль\n/pull - попытка гачи (10 звёзд)\n/pull10 - 10 попыток (90 звёзд)\n/inventory - коллекция\n/help - помощь")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        await update.message.reply_text("Профиль не найден. Используйте /start.")
        return
    text = (
        f"Имя: {pb_user.get('name', '')}\n"
        f"Уровень: {pb_user.get('level', 1)}\n"
        f"Опыт: {pb_user.get('exp', 0)}\n"
        f"Звёзды: {pb_user.get('stars', 0)}\n"
        f"Pity Legendary: {pb_user.get('pity_legendary', 0)}\n"
        f"Pity Void: {pb_user.get('pity_void', 0)}"
    )
    await update.message.reply_text(text)

# --- Гача логика ---
def choose_rarity(pity_legendary, pity_void):
    # Pity: 80 - гарант 5*, 165 - гарант 6*
    if pity_void >= 165:
        return 6
    if pity_legendary >= 80:
        return 5
    return random.choices(RARITY_VALUES, weights=RARITY_WEIGHTS, k=1)[0]

async def pull_once(user, pb_user, update, pull_type="single"):
    pity_legendary = pb_user.get("pity_legendary", 0)
    pity_void = pb_user.get("pity_void", 0)
    stars = pb_user.get("stars", 0)
    user_id = pb_user["id"]

    # Проверка звёзд
    if stars < PULL_COST:
        await update.message.reply_text("Недостаточно звёзд для попытки!")
        return

    rarity = choose_rarity(pity_legendary, pity_void)
    card = pb.get_random_card_by_rarity(rarity)
    if not card:
        await update.message.reply_text(f"Нет карточек с редкостью {rarity}★ в базе!")
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

    # Ответ пользователю
    text = f"Выпала карта: {card['name']} ({card['group']})\nРедкость: {card['rarity']}★"
    if card.get("image_url"):
        await update.message.reply_photo(card["image_url"], caption=text)
    else:
        await update.message.reply_text(text)

async def pull(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        await update.message.reply_text("Профиль не найден. Используйте /start.")
        return
    await pull_once(user, pb_user, update, pull_type="single")

async def pull10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        await update.message.reply_text("Профиль не найден. Используйте /start.")
        return
    stars = pb_user.get("stars", 0)
    if stars < PULL10_COST:
        await update.message.reply_text("Недостаточно звёзд для 10 попыток!")
        return
    # Списываем звёзды сразу
    user_id = pb_user["id"]
    pity_legendary = pb_user.get("pity_legendary", 0)
    pity_void = pb_user.get("pity_void", 0)
    stars -= PULL10_COST
    results = []
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
        results.append(f"{i+1}. {card['name']} ({card['group']}) — {card['rarity']}★")
    pb.update_user_stars_and_pity(user_id, stars, pity_legendary, pity_void)
    await update.message.reply_text("\n".join(results))

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        await update.message.reply_text("Профиль не найден. Используйте /start.")
        return
    user_id = pb_user["id"]
    cards = pb.get_user_inventory(user_id)
    if not cards:
        await update.message.reply_text("Ваша коллекция пуста!")
        return
    # Формируем текстовый список
    lines = []
    for c in cards:
        card = c.get("expand", {}).get("card_id", {})
        if not card:
            continue
        lines.append(f"{card.get('name', '???')} ({card.get('group', '-')}) — {card.get('rarity', '?')}★ ×{c.get('count', 1)}")
    await update.message.reply_text("\n".join(lines))

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("pull", pull))
    app.add_handler(CommandHandler("pull10", pull10))
    app.add_handler(CommandHandler("inventory", inventory))
    app.run_polling()

if __name__ == "__main__":
    main() 