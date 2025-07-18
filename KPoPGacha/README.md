# KPOP Gacha Card Game Bot

## Описание
Telegram-бот для коллекционирования карточек с KPOP-айдолами. Использует Pocketbase для хранения данных.

## Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Заполните `config.py` своими токенами и адресом Pocketbase.
3. Запустите бота:
   ```bash
   python bot.py
   ```

## Структура проекта
- `bot.py` — основной файл Telegram-бота
- `pb_client.py` — клиент для работы с Pocketbase
- `config.py` — настройки токенов и адресов
- `requirements.txt` — зависимости

## Минимальные команды
- `/start` — регистрация и приветствие
- `/help` — справка
- `/profile` — просмотр профиля

---

Pocketbase должен быть запущен и доступен по адресу, указанному в `config.py`. 