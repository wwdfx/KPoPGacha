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