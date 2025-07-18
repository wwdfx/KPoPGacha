import os
import requests
from dotenv import load_dotenv
from bot.config import POCKETBASE_URL, POCKETBASE_USER_EMAIL, POCKETBASE_USER_PASSWORD

load_dotenv()

class PocketbaseClient:
    def __init__(self):
        self.base_url = POCKETBASE_URL.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.login_bot_user(POCKETBASE_USER_EMAIL, POCKETBASE_USER_PASSWORD)

    def login_bot_user(self, email, password):
        url = f"{self.base_url}/api/collections/users/auth-with-password"
        resp = self.session.post(url, json={"identity": email, "password": password})
        resp.raise_for_status()
        data = resp.json()
        self.token = data['token']
        self.session.headers.update({'Authorization': self.token})

    def get(self, path, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.get(url, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.post(url, data=data, json=json, **kwargs)

    # Можно добавить методы put, delete и т.д. по мере необходимости 