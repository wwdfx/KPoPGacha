import httpx
import random
from datetime import datetime, timezone
from math import ceil
from config import POCKETBASE_URL, POCKETBASE_BOT_EMAIL, POCKETBASE_BOT_PASSWORD

class PBClient:
    RANKS = [
        "Стажёр V", "Стажёр IV", "Стажёр III", "Стажёр II", "Стажёр I",
        "Новичок V", "Новичок IV", "Новичок III", "Новичок II", "Новичок I",
        "Восходящая звезда V", "Восходящая звезда IV", "Восходящая звезда III", "Восходящая звезда II", "Восходящая звезда I",
        "Идол V", "Идол IV", "Идол III", "Идол II", "Идол I",
        "Суперзвезда V", "Суперзвезда IV", "Суперзвезда III", "Суперзвезда II", "Суперзвезда I",
        "Легенда"
    ]
    RARITY_EXP = {1: 1, 2: 5, 3: 15, 4: 50, 5: 100, 6: 250}

    def __init__(self):
        self.base_url = POCKETBASE_URL
        self.token = self._login_and_get_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _login_and_get_token(self):
        url = f"{self.base_url}/collections/users/auth-with-password"
        data = {"identity": POCKETBASE_BOT_EMAIL, "password": POCKETBASE_BOT_PASSWORD}
        resp = httpx.post(url, json=data)
        resp.raise_for_status()
        return resp.json()["token"]

    def get_user_by_telegram_id(self, telegram_id):
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return items[0] if items else None

    def create_user(self, telegram_id, name):
        url = f"{self.base_url}/collections/tg_users/records"
        data = {
            "telegram_id": str(telegram_id),
            "name": name,
            "level": 1,
            "exp": 0,
            "stars": 0,
            "pity_legendary": 0,
            "pity_void": 0,
            "last_daily": None
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_all_cards(self):
        url = f"{self.base_url}/collections/cards/records"
        per_page = 500
        page = 1
        all_items = []
        while True:
            params = {"perPage": per_page, "page": page}
            resp = httpx.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            all_items.extend(items)
            if len(items) < per_page:
                break
            page += 1
        return all_items

    def get_random_card_by_rarity(self, rarity):
        url = f"{self.base_url}/collections/cards/records"
        params = {"filter": f'rarity={rarity}'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            return None
        return random.choice(items)

    def add_card_to_user(self, user_id, card_id):
        url = f"{self.base_url}/collections/user_cards/records"
        params = {"filter": f'user_id="{user_id}" && card_id="{card_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/user_cards/records/{record['id']}"
            new_count = max(1, record.get("count", 0)) + 1
            data = {"count": new_count}
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            if resp2.status_code >= 400:
                print(f"PATCH user_cards error: {resp2.status_code} {resp2.text}")
            resp2.raise_for_status()
            return resp2.json()
        else:
            data = {
                "user_id": user_id,
                "card_id": card_id,
                "count": 1,
                "obtained_at": datetime.now(timezone.utc).isoformat()
            }
            resp2 = httpx.post(url, headers=self.headers, json=data)
            if resp2.status_code >= 400:
                print(f"POST user_cards error: {resp2.status_code} {resp2.text}")
            resp2.raise_for_status()
            return resp2.json()

    def update_user_stars_and_pity(self, user_id, stars, pity_legendary, pity_void):
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {"stars": stars, "pity_legendary": pity_legendary, "pity_void": pity_void}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def add_pull_history(self, user_id, card_id, pull_type):
        url = f"{self.base_url}/collections/pull_history/records"
        data = {"user_id": user_id, "card_id": card_id, "pull_type": pull_type}
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_user_inventory(self, user_id):
        url = f"{self.base_url}/collections/user_cards/records"
        params = {
            "filter": f'user_id="{user_id}"',
            "expand": "card_id",
            "perPage": 200
        }
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def check_daily_available(self, pb_user):
        last_daily = pb_user.get("last_daily")
        if not last_daily:
            return True, None
        last_dt = datetime.fromisoformat(last_daily.replace("Z", "+00:00")).date()
        now_dt = datetime.now(timezone.utc).date()
        if last_dt < now_dt:
            return True, None
        return False, last_dt

    def give_daily_reward(self, user_id, current_stars, reward=20):
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        new_stars = current_stars + reward
        data = {"stars": new_stars, "last_daily": datetime.now(timezone.utc).isoformat()}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json(), reward

    def is_first_card(self, user_id, card_id):
        url = f"{self.base_url}/collections/user_cards/records"
        params = {"filter": f'user_id="{user_id}" && card_id="{card_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            return True
        return items[0].get("count", 0) == 0

    def exp_to_next_level(self, level):
        return ceil(100 * (1.15 ** (level - 1)))

    def add_exp_and_check_levelup(self, user_id, current_level, current_exp, add_exp):
        level = current_level
        exp = current_exp + add_exp
        up = False
        while exp >= self.exp_to_next_level(level) and level < len(self.RANKS):
            exp -= self.exp_to_next_level(level)
            level += 1
            up = True
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {"level": level, "exp": exp}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json(), up

    def get_rank(self, level):
        idx = min(level - 1, len(self.RANKS) - 1)
        return self.RANKS[idx]

    def get_pull_history(self, user_id, limit=10):
        url = f"{self.base_url}/collections/pull_history/records"
        params = {
            "filter": f'user_id="{user_id}"',
            "expand": "card_id",
            "sort": "-pulled_at",
            "perPage": limit
        }
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def get_pity_status(self, user_id):
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        user = resp.json()
        return user.get("pity_legendary", 0), user.get("pity_void", 0)

    def get_leaderboard(self, limit=10):
        url = f"{self.base_url}/collections/tg_users/records"
        params = {
            "sort": "-level,-exp",
            "perPage": limit
        }
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def add_card(self, name, group, album, rarity, image_url):
        url = f"{self.base_url}/collections/cards/records"
        data = {
            "name": name,
            "group": group,
            "album": album,
            "rarity": rarity,
            "image_url": image_url,
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def create_auction(self, card_id, seller_id, price, duration_hours):
        from datetime import datetime, timedelta, timezone
        url = f"{self.base_url}/collections/auctions/records"
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(hours=duration_hours)
        data = {
            "card_id": card_id,
            "seller_id": seller_id,
            "price": price,
            "start_time": now.isoformat(),
            "end_time": end_time.isoformat(),
            "status": "active"
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        if resp.status_code >= 400:
            print("AUCTION ERROR:", resp.text)
        resp.raise_for_status()
        return resp.json()

    def get_active_auctions(self):
        url = f"{self.base_url}/collections/auctions/records"
        params = {"filter": 'status="active"', "expand": "card_id,seller_id", "perPage": 50}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def finish_auction(self, auction_id, status="sold", winner_id=None):
        url = f"{self.base_url}/collections/auctions/records/{auction_id}"
        data = {"status": status}
        if winner_id:
            data["winner_id"] = winner_id
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_auction(self, auction_id):
        url = f"{self.base_url}/collections/auctions/records/{auction_id}?expand=card_id,seller_id"
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    # --- PROMO CODE METHODS ---
    def get_promo(self, code):
        url = f"{self.base_url}/collections/promo_codes/records"
        params = {"filter": f'code="{code}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return items[0] if items else None

    def use_promo(self, promo_id, user_id):
        # Получаем текущий used_by
        url = f"{self.base_url}/collections/promo_codes/records/{promo_id}"
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        promo = resp.json()
        used_by = promo.get("used_by", [])
        # Исправление: если used_by строка (один relation), делаем список
        if isinstance(used_by, str):
            used_by = [used_by]
        if user_id in used_by:
            return False  # Уже использовал
        used_by.append(user_id)
        data = {"used_by": used_by}
        resp2 = httpx.patch(url, headers=self.headers, json=data)
        resp2.raise_for_status()
        return True

    def add_promo(self, code, reward, usage_limit=1, is_active=True):
        url = f"{self.base_url}/collections/promo_codes/records"
        data = {
            "code": code,
            "reward": reward,
            "usage_limit": usage_limit,
            "is_active": is_active,
            "used_by": []
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_cards_by_group_album(self, group, album):
        url = f"{self.base_url}/collections/cards/records"
        params = {"filter": f'group="{group}" && album="{album}"', "perPage": 200}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def get_collection_achievement(self, user_id, group, album):
        url = f"{self.base_url}/collections/collection_achievements/records"
        params = {"filter": f'user_id="{user_id}" && group="{group}" && album="{album}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return items[0] if items else None

    def set_collection_achievement(self, user_id, group, album, level):
        ach = self.get_collection_achievement(user_id, group, album)
        url = f"{self.base_url}/collections/collection_achievements/records"
        data = {"user_id": user_id, "group": group, "album": album, "level": level}
        if ach:
            patch_url = f"{url}/{ach['id']}"
            resp = httpx.patch(patch_url, headers=self.headers, json={"level": level})
            resp.raise_for_status()
            return resp.json()
        else:
            resp = httpx.post(url, headers=self.headers, json=data)
            resp.raise_for_status()
            return resp.json()

    def get_all_users(self):
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"perPage": 500}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def set_daily_bonus_token(self, user_id, token):
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        from datetime import datetime, timezone
        data = {"daily_bonus_token": token, "daily_bonus_date": datetime.now(timezone.utc).date().isoformat()}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def check_and_consume_daily_bonus(self, user_id, token):
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        user = resp.json()
        from datetime import datetime, timezone
        today = datetime.now(timezone.utc).date().isoformat()
        if user.get("daily_bonus_token") == token and user.get("daily_bonus_date") == today:
            # Сбросить токен, выдать бонус
            patch = {"daily_bonus_token": "", "daily_bonus_date": today}
            httpx.patch(url, headers=self.headers, json=patch)
            return True
        return False

    def set_active_banner(self, user_id, group, album):
        """Установить пользователю активный баннер (группа+альбом)."""
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {"active_banner_group": group, "active_banner_album": album}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def reset_active_banner(self, user_id):
        """Сбросить активный баннер (общий пулл)."""
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {"active_banner_group": None, "active_banner_album": None}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_active_banner(self, pb_user):
        """Получить активный баннер пользователя. Если не выбран — вернуть случайный существующий баннер (group, album)."""
        group = pb_user.get("active_banner_group")
        album = pb_user.get("active_banner_album")
        if group and album:
            return group, album
        # Если не выбран — выбрать случайный баннер
        all_cards = self.get_all_cards()
        if not all_cards:
            return None, None
        banners = [(c["group"], c["album"]) for c in all_cards if c.get("group") and c.get("album")]
        if not banners:
            return None, None
        return random.choice(banners)

    def ban_user(self, telegram_id, reason):
        """Заблокировать пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {"banned": True, "ban_reason": reason}
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()
            return resp2.json()
        return None

    def unban_user(self, telegram_id):
        """Разблокировать пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {"banned": False, "ban_reason": None}
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()
            return resp2.json()
        return None

    def reset_user_progress(self, telegram_id):
        """Сбросить прогресс пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {
                "level": 1,
                "exp": 0,
                "stars": 0,
                "pity_legendary": 0,
                "pity_void": 0
            }
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()

            # Удаляем все карточки пользователя
            user_id = record["id"]
            self.delete_user_cards(user_id)

            return resp2.json()
        return None

    def set_user_level(self, telegram_id, level):
        """Установить уровень пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {"level": level}
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()
            return resp2.json()
        return None

    def set_user_exp(self, telegram_id, exp):
        """Установить опыт пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {"exp": exp}
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()
            return resp2.json()
        return None

    def delete_user_cards(self, user_id):
        """Удалить все карточки пользователя"""
        url = f"{self.base_url}/collections/user_cards/records"
        params = {"filter": f'user_id="{user_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        for item in items:
            delete_url = f"{self.base_url}/collections/user_cards/records/{item['id']}"
            httpx.delete(delete_url, headers=self.headers)

    def get_card_by_id(self, card_id):
        """Получить карточку по ID"""
        url = f"{self.base_url}/collections/cards/records"
        params = {"filter": f'id="{card_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return items[0] if items else None

    def add_card_to_user(self, user_id, card_id):
        """Добавить карточку пользователю"""
        url = f"{self.base_url}/collections/user_cards/records"
        data = {
            "user_id": user_id,
            "card_id": card_id,
            "quantity": 1
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def remove_card_from_user(self, user_id, card_id):
        """Удалить карточку у пользователя"""
        url = f"{self.base_url}/collections/user_cards/records"
        params = {"filter": f'user_id="{user_id}" && card_id="{card_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            delete_url = f"{self.base_url}/collections/user_cards/records/{items[0]['id']}"
            httpx.delete(delete_url, headers=self.headers)
            return True
        return False

    def duplicate_card_for_user(self, user_id, card_id, count):
        """Добавить несколько копий карточки пользователю"""
        url = f"{self.base_url}/collections/user_cards/records"
        params = {"filter": f'user_id="{user_id}" && card_id="{card_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])

        if items:
            # Обновляем количество существующей записи
            record = items[0]
            current_quantity = record.get("quantity", 1)
            new_quantity = current_quantity + count
            update_url = f"{self.base_url}/collections/user_cards/records/{record['id']}"
            data = {"quantity": new_quantity}
            httpx.patch(update_url, headers=self.headers, json=data)
        else:
            # Создаем новую запись
            data = {
                "user_id": user_id,
                "card_id": card_id,
                "quantity": count
            }
            httpx.post(url, headers=self.headers, json=data)

    def set_user_pity(self, telegram_id, legendary, void):
        """Установить pity пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {
                "pity_legendary": legendary,
                "pity_void": void
            }
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()
            return resp2.json()
        return None

    def reset_daily_bonus(self, user_id):
        """Сбросить ежедневный бонус пользователя"""
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {"last_daily": None}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def set_user_banner(self, telegram_id, group, album):
        """Установить баннер пользователя"""
        url = f"{self.base_url}/collections/tg_users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if items:
            record = items[0]
            update_url = f"{self.base_url}/collections/tg_users/records/{record['id']}"
            data = {
                "active_banner_group": group,
                "active_banner_album": album
            }
            resp2 = httpx.patch(update_url, headers=self.headers, json=data)
            resp2.raise_for_status()
            return resp2.json()
        return None

    def reset_user_banner(self, user_id):
        """Сбросить баннер пользователя"""
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {
            "active_banner_group": None,
            "active_banner_album": None
        }
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def give_achievement(self, user_id, group, album, level):
        """Выдать достижение пользователю"""
        url = f"{self.base_url}/collections/collection_achievements/records"
        data = {
            "user_id": user_id,
            "group": group,
            "album": album,
            "level": level,
            "achieved_at": datetime.now().isoformat()
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def reset_user_achievements(self, user_id):
        """Сбросить достижения пользователя"""
        url = f"{self.base_url}/collections/collection_achievements/records"
        params = {"filter": f'user_id="{user_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        for item in items:
            delete_url = f"{self.base_url}/collections/collection_achievements/records/{item['id']}"
            httpx.delete(delete_url, headers=self.headers)
        return True

    def get_card_ownership_stats(self, card_id):
        """Получить статистику владения карточкой"""
        url = f"{self.base_url}/collections/user_cards/records"
        params = {"filter": f'card_id="{card_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])

        total_copies = sum(item.get("quantity", 1) for item in items)
        total_owners = len(items)

        return {
            "total_owners": total_owners,
            "total_copies": total_copies
        }

    def get_activity_stats(self, days):
        """Получить статистику активности"""
        from datetime import datetime, timedelta

        # Получаем всех пользователей
        users = self.get_all_users()

        # Получаем историю попыток
        url = f"{self.base_url}/collections/pull_history/records"
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        pull_history = resp.json().get("items", [])

        # Вычисляем даты
        now = datetime.now()
        days_ago = now - timedelta(days=days)
        today = now.date()

        # Фильтруем попытки по дате
        recent_pulls = []
        today_pulls = 0

        for pull in pull_history:
            try:
                pull_date = datetime.fromisoformat(pull.get("created", "").replace("Z", "+00:00"))
                if pull_date >= days_ago:
                    recent_pulls.append(pull)
                    if pull_date.date() == today:
                        today_pulls += 1
            except:
                continue

        # Подсчитываем статистику
        new_users = 0
        active_users = set()

        for user in users:
            try:
                created_date = datetime.fromisoformat(user.get("created", "").replace("Z", "+00:00"))
                if created_date >= days_ago:
                    new_users += 1
            except:
                continue

            # Проверяем активность пользователя
            user_pulls = [p for p in recent_pulls if p.get("user_id") == user["id"]]
            if user_pulls:
                active_users.add(user["id"])

        total_pulls = len(recent_pulls)
        avg_pulls_per_user = total_pulls / len(active_users) if active_users else 0

        return {
            "new_users": new_users,
            "active_users": len(active_users),
            "total_pulls": total_pulls,
            "avg_pulls_per_user": avg_pulls_per_user,
            "pulls_today": today_pulls
        }

    def create_backup(self):
        """Создать резервную копию данных"""
        from datetime import datetime

        # Получаем статистику по всем коллекциям
        users = self.get_all_users()
        cards = self.get_all_cards()

        # Получаем другие данные
        url_pulls = f"{self.base_url}/collections/pull_history/records"
        resp_pulls = httpx.get(url_pulls, headers=self.headers)
        resp_pulls.raise_for_status()
        pulls = resp_pulls.json().get("items", [])

        url_auctions = f"{self.base_url}/collections/auctions/records"
        resp_auctions = httpx.get(url_auctions, headers=self.headers)
        resp_auctions.raise_for_status()
        auctions = resp_auctions.json().get("items", [])

        url_achievements = f"{self.base_url}/collections/collection_achievements/records"
        resp_achievements = httpx.get(url_achievements, headers=self.headers)
        resp_achievements.raise_for_status()
        achievements = resp_achievements.json().get("items", [])

        return {
            "users_count": len(users),
            "cards_count": len(cards),
            "pulls_count": len(pulls),
            "auctions_count": len(auctions),
            "achievements_count": len(achievements),
            "created_at": datetime.now().isoformat()
        }

    def set_maintenance_mode(self, enabled):
        """Установить режим обслуживания"""
        # В реальной реализации здесь можно сохранить флаг в базе данных
        # или использовать глобальную переменную
        # Пока что просто возвращаем успех
        return True

    def start_event(self, event_name, duration_days):
        """Запустить праздничное событие"""
        from datetime import datetime, timedelta

        end_date = datetime.now() + timedelta(days=duration_days)

        # В реальной реализации здесь можно создать запись в базе данных
        # Пока что возвращаем заглушку
        return {
            "id": f"event_{datetime.now().timestamp()}",
            "name": event_name,
            "end_date": end_date.isoformat(),
            "duration_days": duration_days
        }

    def end_active_event(self):
        """Завершить активное событие"""
        from datetime import datetime

        # В реальной реализации здесь можно найти и завершить активное событие
        # Пока что возвращаем заглушку
        return {
            "name": "Тестовое событие",
            "participants_count": 0,
            "ended_at": datetime.now().isoformat()
        }

    def give_event_rewards(self, event_name):
        """Выдать награды участникам события"""
        # В реальной реализации здесь можно выдать награды участникам
        # Пока что возвращаем заглушку
        return {
            "participants_count": 0,
            "rewards_given": 0,
            "stars_given": 0
        }

    def set_event_banner(self, group, album):
        """Установить баннер события"""
        # Получаем количество карточек в баннере
        cards = self.get_cards_by_group_album(group, album)

        return {
            "cards_count": len(cards)
        }

    def add_warning(self, telegram_id, reason):
        """Добавить предупреждение пользователю"""
        from datetime import datetime

        # В реальной реализации здесь можно создать запись в базе данных
        # Пока что просто возвращаем успех
        return True

    def mute_user(self, telegram_id, hours):
        """Замутить пользователя"""
        from datetime import datetime, timedelta

        # В реальной реализации здесь можно обновить запись пользователя
        # Пока что просто возвращаем успех
        return True

    def unmute_user(self, telegram_id):
        """Размутить пользователя"""
        # В реальной реализации здесь можно обновить запись пользователя
        # Пока что просто возвращаем успех
        return True

    def get_user_moderation_history(self, telegram_id):
        """Получить историю модерации пользователя"""
        # В реальной реализации здесь можно получить записи из базы данных
        # Пока что возвращаем пустой список
        return []

    def get_daily_report(self):
        """Получить ежедневный отчет"""
        from datetime import datetime, timedelta
        
        # Получаем данные за сегодня
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # В реальной реализации здесь можно получить данные из базы
        # Пока что возвращаем заглушку
        return {
            "new_users": 0,
            "active_users": 0,
            "total_pulls": 0,
            "single_pulls": 0,
            "ten_pulls": 0,
            "stars_given": 0,
            "stars_earned": 0,
            "auctions_created": 0,
            "auctions_completed": 0,
            "promos_used": 0
        }

    def get_weekly_report(self):
        """Получить еженедельный отчет"""
        from datetime import datetime, timedelta
        
        # Получаем данные за последнюю неделю
        week_ago = datetime.now() - timedelta(days=7)
        
        # В реальной реализации здесь можно получить данные из базы
        # Пока что возвращаем заглушку
        return {
            "new_users": 0,
            "active_users": 0,
            "total_pulls": 0,
            "avg_pulls_per_user": 0.0,
            "stars_given": 0,
            "stars_earned": 0,
            "auctions_created": 0,
            "auctions_completed": 0,
            "promos_used": 0,
            "achievements_given": 0
        }

    def get_revenue_stats(self):
        """Получить статистику доходов"""
        # Получаем всех пользователей
        users = self.get_all_users()
        
        if not users:
            return {
                "total_stars": 0,
                "avg_stars_per_user": 0.0,
                "max_stars": 0,
                "users_with_zero_stars": 0,
                "users_with_100_plus_stars": 0,
                "users_with_1000_plus_stars": 0
            }
        
        total_stars = sum(user.get("stars", 0) for user in users)
        max_stars = max(user.get("stars", 0) for user in users)
        users_with_zero_stars = sum(1 for user in users if user.get("stars", 0) == 0)
        users_with_100_plus_stars = sum(1 for user in users if user.get("stars", 0) >= 100)
        users_with_1000_plus_stars = sum(1 for user in users if user.get("stars", 0) >= 1000)
        avg_stars_per_user = total_stars / len(users)
        
        return {
            "total_stars": total_stars,
            "avg_stars_per_user": avg_stars_per_user,
            "max_stars": max_stars,
            "users_with_zero_stars": users_with_zero_stars,
            "users_with_100_plus_stars": users_with_100_plus_stars,
            "users_with_1000_plus_stars": users_with_1000_plus_stars
        }

    def get_popular_cards(self, limit=10):
        """Получить популярные карточки"""
        # Заглушка - возвращаем случайные карточки
        all_cards = self.get_all_cards()
        if len(all_cards) <= limit:
            return all_cards
        return random.sample(all_cards, limit)

    # Функции для управления интерактивами
    def create_interactive_post(self, post_url, title, description, reward_stars=15, total_answers=15, reward_per_answer=15):
        """Создать новый интерактивный пост"""
        url = f"{self.base_url}/collections/interactive_posts/records"
        data = {
            "post_url": post_url,
            "title": title,
            "description": description,
            "reward_stars": reward_stars,
            "total_answers": total_answers,
            "reward_per_answer": reward_per_answer,
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_active_interactive_posts(self):
        """Получить все активные интерактивные посты"""
        url = f"{self.base_url}/collections/interactive_posts/records"
        params = {"filter": "is_active=true"}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def get_interactive_post(self, post_id):
        """Получить интерактивный пост по ID"""
        url = f"{self.base_url}/collections/interactive_posts/records/{post_id}"
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def deactivate_interactive_post(self, post_id):
        """Деактивировать интерактивный пост"""
        url = f"{self.base_url}/collections/interactive_posts/records/{post_id}"
        data = {"is_active": False}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def delete_interactive_post(self, post_id):
        """Удалить интерактивный пост"""
        url = f"{self.base_url}/collections/interactive_posts/records/{post_id}"
        resp = httpx.delete(url, headers=self.headers)
        resp.raise_for_status()
        return True

    def check_user_interactive_claim(self, user_id, post_id):
        """Проверить, получил ли пользователь награду за интерактив"""
        url = f"{self.base_url}/collections/interactive_claims/records"
        params = {"filter": f'user_id="{user_id}" && post_id="{post_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return len(items) > 0

    def claim_interactive_reward(self, user_id, post_id, reward_stars, answers_count=0):
        """Записать получение награды за интерактив"""
        url = f"{self.base_url}/collections/interactive_claims/records"
        data = {
            "user_id": user_id,
            "post_id": post_id,
            "reward_stars": reward_stars,
            "answers_count": answers_count,
            "claimed_at": datetime.now(timezone.utc).isoformat()
        }
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_user_interactive_claims(self, user_id):
        """Получить все интерактивы, за которые пользователь получил награду"""
        url = f"{self.base_url}/collections/interactive_claims/records"
        params = {"filter": f'user_id="{user_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])

    def get_interactive_stats(self):
        """Получить статистику по интерактивам"""
        try:
            # Получаем все активные интерактивы
            active_interactives = self.get_active_interactive_posts()
            
            # Получаем все записи о наградах
            url = f"{self.base_url}/collections/interactive_claims/records"
            resp = httpx.get(url, headers=self.headers)
            resp.raise_for_status()
            all_claims = resp.json().get("items", [])
            
            stats = {
                "total_interactives": len(active_interactives),
                "total_claims": len(all_claims),
                "total_rewards_given": sum(claim.get("reward_stars", 0) for claim in all_claims),
                "interactives": []
            }
            
            for interactive in active_interactives:
                post_id = interactive["id"]
                post_claims = [claim for claim in all_claims if claim.get("post_id") == post_id]
                
                interactive_stats = {
                    "id": post_id,
                    "title": interactive["title"],
                    "total_answers": interactive.get("total_answers", 15),
                    "reward_per_answer": interactive.get("reward_per_answer", 15),
                    "max_reward": interactive.get("total_answers", 15) * interactive.get("reward_per_answer", 15),
                    "claims_count": len(post_claims),
                    "total_rewarded": sum(claim.get("reward_stars", 0) for claim in post_claims)
                }
                stats["interactives"].append(interactive_stats)
            
            return stats
            
        except Exception as e:
            print(f"Error getting interactive stats: {e}")
            return None

    def get_user_achievements(self, user_id):
        """Получить достижения пользователя"""
        url = f"{self.base_url}/collections/collection_achievements/records"
        params = {"filter": f'user_id="{user_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json().get("items", []) 