import httpx
from config import POCKETBASE_URL, POCKETBASE_BOT_EMAIL, POCKETBASE_BOT_PASSWORD

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