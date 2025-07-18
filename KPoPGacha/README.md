# KPoPGacha Bot

Telegram-бот для гача-игры по коллекционированию карточек с KPOP-айдолами.

## Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Скопируйте `.env.example` в `.env` и заполните токены.
3. Запустите бота:
   ```bash
   python -m bot.main
   ```

## Структура проекта
- `bot/` — исходный код бота
- `requirements.txt` — зависимости
- `.env` — переменные окружения (токены, url Pocketbase)

## Требования
- Python 3.10+
- Pocketbase (запущенный инстанс) 