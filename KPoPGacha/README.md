# KPOP Gacha Card Game Telegram Bot

## Описание

Это Telegram-бот для коллекционирования карточек KPOP айдолов. Игроки могут собирать карточки, управлять коллекцией, зарабатывать игровую валюту (звёзды), повышать уровень, участвовать в аукционах и соревноваться с другими пользователями.

Бот реализован на Python с использованием библиотеки [`python-telegram-bot`](https://python-telegram-bot.org/) и использует [Pocketbase](https://pocketbase.io/) как backend-базу данных.

---

## Основные возможности

- **Гача-пуллы**: /pull (1 карта), /pull10 (10 карт) с шансами по редкости и системой "жалости" (pity).
- **Профиль**: /profile — уровень, опыт, звёзды, ранг, pity-счётчики.
- **Инвентарь**: просмотр коллекции по группам и альбомам, отображение всех и недостающих карт, процент заполнения.
- **Дубликаты**: массовый обмен дубликатов на звёзды с учётом редкости.
- **Аукцион**: выставление карт на продажу, покупка, уведомления в канал.
- **Достижения**: за заполнение коллекций (25/50/75/100% по альбому), награды за прогресс.
- **Промокоды**: ввод и активация промокодов, лимиты и награды.
- **Ежедневный бонус**: /daily и рассылка уникальных бонус-ссылок.
- **Лидерборд**: топ-10 игроков по уровню/опыту.
- **История**: последние 10 пуллов.
- **Настройки**: /settings (заглушка).
- **Меню**: /menu с инлайн-кнопками для всех функций.
- **Админ-команды**: /addcard, /addpromo, /drop100, ручная рассылка бонусов.

---

## Структура проекта

```
KPoPGacha/
├── bot.py                # Основная логика Telegram-бота
├── pb_client.py          # Работа с Pocketbase API
├── config.py             # Конфигурация (токены, константы)
├── requirements.txt      # Зависимости Python
├── start.sh              # Скрипт запуска и установки окружения
├── .gitignore            # Исключения для git
├── grant_achievements.py # Скрипт для ретро-выдачи достижений
├── grant_daily_bonus_links.py # Скрипт рассылки бонус-ссылок
└── README.md             # Описание проекта (этот файл)
```

---

## Структура коллекций Pocketbase

### tg_users
- `id` (text)
- `telegram_id` (text)
- `name` (text)
- `level` (int)
- `exp` (int)
- `stars` (int)
- `pity_legendary` (int)
- `pity_void` (int)
- `last_daily` (date)
- `daily_bonus_token` (text) *(для бонус-ссылок)*
- `daily_bonus_date` (date) *(для бонус-ссылок)*
- `active_banner_group` (text, nullable) *(выбранная группа баннера)*
- `active_banner_album` (text, nullable) *(выбранный альбом баннера)*

### cards
- `id` (text)
- `name` (text)
- `group` (text)
- `album` (text)
- `rarity` (int)
- `image_url` (text)

### user_cards
- `id` (text)
- `user_id` (relation → tg_users)
- `card_id` (relation → cards)
- `count` (int)
- `obtained_at` (date)

### pull_history
- `id` (text)
- `user_id` (relation → tg_users)
- `card_id` (relation → cards)
- `pull_type` (text)
- `created` (date)

### auctions
- `id` (text)
- `card_id` (relation → cards)
- `seller_id` (relation → tg_users)
- `buyer_id` (relation → tg_users, nullable)
- `price` (int)
- `duration` (int, часы)
- `status` (text: active/sold/expired)
- `created` (date)

### promo_codes
- `id` (text)
- `code` (text)
- `reward` (int)
- `is_active` (bool)
- `usage_limit` (int)
- `used_by` (array of relation → tg_users)

### collection_achievements
- `id` (text)
- `user_id` (relation → tg_users)
- `group` (text)
- `album` (text)
- `level` (int, 1-4)

---

## Технические детали

- Python 3.10+
- python-telegram-bot 20+
- Pocketbase 0.18+
- Pillow (обработка изображений)
- requests (загрузка изображений)

---

## TODO / WIP
- [ ] Промокоды: коллекция, команды, UI, методы в pb_client.py
- [ ] Массовый обмен дубликатов
- [ ] Ежедневные бонус-ссылки (доработка)
- [ ] Улучшения UI и новые функции

---

## Запуск

```bash
cd KPoPGacha
bash start.sh
```

---

## Контакты

Вопросы и предложения: @your_telegram 