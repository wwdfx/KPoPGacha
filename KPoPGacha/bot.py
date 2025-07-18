from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pb_client import PBClient
from config import TELEGRAM_BOT_TOKEN

pb = PBClient()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pb_user = pb.get_user_by_telegram_id(user.id)
    if not pb_user:
        pb.create_user(user.id, user.full_name)
        await update.message.reply_text(f"Добро пожаловать, {user.full_name}! Ваш игровой профиль создан.")
    else:
        await update.message.reply_text(f"С возвращением, {user.full_name}!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - начать\n/profile - профиль\n/help - помощь")

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

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile))
    app.run_polling()

if __name__ == "__main__":
    main() 