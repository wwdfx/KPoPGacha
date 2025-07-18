import httpx
import random
from datetime import datetime, timezone
from math import ceil
from config import POCKETBASE_URL, POCKETBASE_BOT_EMAIL, POCKETBASE_BOT_PASSWORD

RANKS = [
    "Стажёр V", "Стажёр IV", "Стажёр III", "Стажёр II", "Стажёр I",
    "Новичок V", "Новичок IV", "Новичок III", "Новичок II", "Новичок I",
    "Восходящая звезда V", "Восходящая звезда IV", "Восходящая звезда III", "Восходящая звезда II", "Восходящая звезда I",
    "Идол V", "Идол IV", "Идол III", "Идол II", "Идол I",
    "Суперзвезда V", "Суперзвезда IV", "Суперзвезда III", "Суперзвезда II", "Суперзвезда I",
    "Легенда"
]

RARITY_EXP = {1: 1, 2: 5, 3: 15, 4: 50, 5: 100, 6: 250}

class PBClient:
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
        resp = httpx.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json().get("items", [])

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
            resp2.raise_for_status()
            return resp2.json()
        else:
            data = {"user_id": user_id, "card_id": card_id, "count": 1}
            resp2 = httpx.post(url, headers=self.headers, json=data)
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
        while exp >= self.exp_to_next_level(level) and level < len(RANKS):
            exp -= self.exp_to_next_level(level)
            level += 1
            up = True
        url = f"{self.base_url}/collections/tg_users/records/{user_id}"
        data = {"level": level, "exp": exp}
        resp = httpx.patch(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json(), up

    def get_rank(self, level):
        idx = min(level - 1, len(RANKS) - 1)
        return RANKS[idx]

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