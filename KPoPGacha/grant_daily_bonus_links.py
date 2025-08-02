from pb_client import PBClient
import uuid
from config import TELEGRAM_BOT_TOKEN
from telegram import Bot

pb = PBClient()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
bot_username = 'kpop_gacha_bot'  # Укажи username бота без @

def main():
    users = pb.get_all_users()
    for user in users:
        user_id = user["id"]
        tg_id = user["telegram_id"]
        token = str(uuid.uuid4())
        pb.set_daily_bonus_token(user_id, token)
        link = f"https://t.me/{bot_username}?start=bonus_{tg_id}_{token}"
        try:
            bot.send_message(chat_id=int(tg_id), text=f"🌟 Ваш ежедневный бонус! Жмите на кнопку ниже, чтобы получить 25 звёзд!", reply_markup={"inline_keyboard": [[{"text": "Получить бонус", "url": link}]]})
        except Exception as e:
            print(f"Не удалось отправить бонус пользователю: {tg_id}: {e}")

if __name__ == "__main__":
    main() 