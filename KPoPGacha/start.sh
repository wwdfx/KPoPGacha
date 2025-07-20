#!/bin/bash
set -e

# Создать виртуальное окружение, если не существует
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Активировать виртуальное окружение
source .venv/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Запустить бота
python bot.py 