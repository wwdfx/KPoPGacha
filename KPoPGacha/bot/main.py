import os
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
from bot.commands import get_handlers

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    for handler in get_handlers():
        application.add_handler(handler)
    application.run_polling()

if __name__ == '__main__':
    main() 