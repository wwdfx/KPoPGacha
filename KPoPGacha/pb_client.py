import httpx
from config import POCKETBASE_URL, POCKETBASE_ADMIN_TOKEN

class PBClient:
    def __init__(self):
        self.base_url = POCKETBASE_URL
        self.headers = {"Authorization": f"Admin {POCKETBASE_ADMIN_TOKEN}"}

    def get_user_by_telegram_id(self, telegram_id):
        url = f"{self.base_url}/collections/users/records"
        params = {"filter": f'telegram_id="{telegram_id}"'}
        resp = httpx.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return items[0] if items else None

    def create_user(self, telegram_id, name):
        url = f"{self.base_url}/collections/users/records"
        data = {"telegram_id": str(telegram_id), "name": name}
        resp = httpx.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json() 