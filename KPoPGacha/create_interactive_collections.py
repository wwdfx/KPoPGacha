#!/usr/bin/env python3
"""
Скрипт для создания коллекций интерактивов в Pocketbase
Запустите этот скрипт после настройки Pocketbase
"""

import requests
import json
from config import POCKETBASE_URL, POCKETBASE_BOT_EMAIL, POCKETBASE_BOT_PASSWORD

def login_to_pocketbase():
    """Вход в Pocketbase для получения токена администратора"""
    url = f"{POCKETBASE_URL}/api/admins/auth-with-password"
    data = {
        "identity": POCKETBASE_BOT_EMAIL,
        "password": POCKETBASE_BOT_PASSWORD
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["token"]
    except Exception as e:
        print(f"Ошибка входа в Pocketbase: {e}")
        return None

def create_collection(token, collection_data):
    """Создание коллекции в Pocketbase"""
    url = f"{POCKETBASE_URL}/api/collections"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=collection_data)
        if response.status_code == 200:
            print(f"✅ Коллекция '{collection_data['name']}' создана успешно!")
            return True
        else:
            print(f"❌ Ошибка создания коллекции '{collection_data['name']}': {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при создании коллекции '{collection_data['name']}': {e}")
        return False

def main():
    print("🔧 Создание коллекций для интерактивов в Pocketbase...")
    
    # Вход в систему
    token = login_to_pocketbase()
    if not token:
        print("❌ Не удалось войти в Pocketbase. Проверьте настройки в config.py")
        return
    
    print("✅ Успешный вход в Pocketbase")
    
    # Данные для коллекции interactive_posts
    interactive_posts_collection = {
        "name": "interactive_posts",
        "type": "base",
        "system": False,
        "schema": [
            {
                "id": "post_url",
                "name": "post_url",
                "type": "text",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "pattern": ""
                }
            },
            {
                "id": "title",
                "name": "title",
                "type": "text",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "pattern": ""
                }
            },
            {
                "id": "description",
                "name": "description",
                "type": "text",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "pattern": ""
                }
            },
            {
                "id": "reward_stars",
                "name": "reward_stars",
                "type": "number",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "noDecimal": True
                }
            },
            {
                "id": "total_answers",
                "name": "total_answers",
                "type": "number",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "noDecimal": True
                }
            },
            {
                "id": "reward_per_answer",
                "name": "reward_per_answer",
                "type": "number",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "noDecimal": True
                }
            },
            {
                "id": "is_active",
                "name": "is_active",
                "type": "bool",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {}
            },
            {
                "id": "created_at",
                "name": "created_at",
                "type": "date",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": "",
                    "max": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "@request.auth.id != \"\"",
        "viewRule": "@request.auth.id != \"\"",
        "createRule": "@request.auth.id != \"\"",
        "updateRule": "@request.auth.id != \"\"",
        "deleteRule": "@request.auth.id != \"\"",
        "options": {}
    }
    
    # Данные для коллекции interactive_claims
    interactive_claims_collection = {
        "name": "interactive_claims",
        "type": "base",
        "system": False,
        "schema": [
            {
                "id": "user_id",
                "name": "user_id",
                "type": "relation",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "collectionId": "tg_users",
                    "cascadeDelete": False,
                    "minSelect": None,
                    "maxSelect": 1,
                    "displayFields": None
                }
            },
            {
                "id": "post_id",
                "name": "post_id",
                "type": "relation",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "collectionId": "interactive_posts",
                    "cascadeDelete": False,
                    "minSelect": None,
                    "maxSelect": 1,
                    "displayFields": None
                }
            },
            {
                "id": "reward_stars",
                "name": "reward_stars",
                "type": "number",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "noDecimal": True
                }
            },
            {
                "id": "answers_count",
                "name": "answers_count",
                "type": "number",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": None,
                    "max": None,
                    "noDecimal": True
                }
            },
            {
                "id": "claimed_at",
                "name": "claimed_at",
                "type": "date",
                "system": False,
                "required": True,
                "presentable": False,
                "unique": False,
                "options": {
                    "min": "",
                    "max": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "@request.auth.id != \"\"",
        "viewRule": "@request.auth.id != \"\"",
        "createRule": "@request.auth.id != \"\"",
        "updateRule": "@request.auth.id != \"\"",
        "deleteRule": "@request.auth.id != \"\"",
        "options": {}
    }
    
    # Создание коллекций
    success_count = 0
    
    if create_collection(token, interactive_posts_collection):
        success_count += 1
    
    if create_collection(token, interactive_claims_collection):
        success_count += 1
    
    print(f"\n📊 Результат: {success_count}/2 коллекций создано успешно")
    
    if success_count == 2:
        print("✅ Все коллекции созданы! Теперь можно использовать команды интерактивов.")
    else:
        print("⚠️ Некоторые коллекции не были созданы. Проверьте логи выше.")

if __name__ == "__main__":
    main() 