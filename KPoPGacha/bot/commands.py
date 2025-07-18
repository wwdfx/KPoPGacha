from bot.pb_client import PocketbaseClient
from telegram.ext import CommandHandler

pb = PocketbaseClient()

async def start(update, context):
    await update.message.reply_text('Добро пожаловать в KPoPGacha!')

async def help_command(update, context):
    await update.message.reply_text('Список команд:\n/start — начать\n/help — помощь\n/profile — ваш профиль')

async def profile(update, context):
    user = update.effective_user
    telegram_id = str(user.id)
    username = user.username or user.full_name or "User"
    # Проверяем, есть ли пользователь в базе
    resp = pb.get(f"/api/collections/users/records?filter=telegram_id='{telegram_id}'")
    data = resp.json()
    if data['totalItems'] == 0:
        # Регистрируем нового пользователя
        user_data = {
            "username": username,
            "telegram_id": telegram_id,
            "level": 1,
            "exp": 0,
            "stars": 0,
            "pity_legendary": 0,
            "pity_void": 0
        }
        create_resp = pb.post("/api/collections/users/records", json=user_data)
        user_info = create_resp.json()
    else:
        user_info = data['items'][0]
    text = (
        f"👤 <b>{username}</b>\n"
        f"Уровень: <b>{user_info.get('level', 1)}</b>\n"
        f"Опыт: <b>{user_info.get('exp', 0)}</b>\n"
        f"Звёзды: <b>{user_info.get('stars', 0)}</b>\n"
        f"Жалость (5★): <b>{user_info.get('pity_legendary', 0)}</b>\n"
        f"Жалость (6★): <b>{user_info.get('pity_void', 0)}</b>"
    )
    await update.message.reply_html(text)

def get_handlers():
    return [
        CommandHandler('start', start),
        CommandHandler('help', help_command),
        CommandHandler('profile', profile),
    ] 