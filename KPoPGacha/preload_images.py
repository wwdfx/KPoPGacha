#!/usr/bin/env python3
"""
Скрипт для предварительного скачивания всех изображений карточек
"""

import os
import hashlib
import requests
import time
from pb_client import PBClient

# Создаем папку для кэша изображений
CACHE_DIR = "image_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cached_image_path(image_url):
    """Получает путь к кэшированному изображению или скачивает его"""
    if not image_url:
        return None
    
    # Создаем хеш URL для имени файла
    url_hash = hashlib.md5(image_url.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{url_hash}.jpg")
    
    # Если файл уже существует, возвращаем его
    if os.path.exists(cache_path):
        return cache_path
    
    return None

def download_image(image_url):
    """Скачивает изображение с ограничениями по скорости"""
    if not image_url:
        return None
    
    # Создаем хеш URL для имени файла
    url_hash = hashlib.md5(image_url.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{url_hash}.jpg")
    
    # Если файл уже существует, пропускаем
    if os.path.exists(cache_path):
        return cache_path
    
    # Скачиваем изображение с ограничениями
    try:
        print(f"Скачиваю: {image_url}")
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        with open(cache_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Сохранено: {cache_path}")
        return cache_path
    except Exception as e:
        print(f"✗ Ошибка скачивания {image_url}: {e}")
        return None

def main():
    print("🚀 Начинаю предварительное скачивание изображений карточек...")
    
    # Подключаемся к базе
    pb = PBClient()
    
    # Получаем все карточки
    print("📋 Получаю список всех карточек из базы...")
    all_cards = pb.get_all_cards()
    print(f"Найдено {len(all_cards)} карточек")
    
    # Собираем уникальные URL изображений
    image_urls = set()
    for card in all_cards:
        if card.get("image_url"):
            image_urls.add(card["image_url"])
    
    print(f"Найдено {len(image_urls)} уникальных изображений")
    
    # Скачиваем изображения с ограничениями
    downloaded = 0
    skipped = 0
    failed = 0
    
    for i, image_url in enumerate(image_urls, 1):
        print(f"\n[{i}/{len(image_urls)}] Обрабатываю изображение...")
        
        # Проверяем, есть ли уже в кэше
        if get_cached_image_path(image_url):
            print(f"⏭️  Уже в кэше, пропускаю")
            skipped += 1
            continue
        
        # Скачиваем с задержкой
        result = download_image(image_url)
        if result:
            downloaded += 1
        else:
            failed += 1
        
        # Задержка между запросами (1 секунда)
        if i < len(image_urls):
            print("⏳ Жду 1 секунду...")
            time.sleep(1)
    
    print(f"\n🎉 Завершено!")
    print(f"📥 Скачано: {downloaded}")
    print(f"⏭️  Пропущено (уже в кэше): {skipped}")
    print(f"❌ Ошибок: {failed}")
    print(f"📁 Все изображения сохранены в папке: {CACHE_DIR}")

if __name__ == "__main__":
    main() 