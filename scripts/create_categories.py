import requests

CATEGORY_URL = "http://127.0.0.1:8000/category/"
LOGIN_URL = "http://127.0.0.1:8000/auth/login"

USER_EMAIL = "pivo@gmail.com"
USER_PASSWORD = "1234567890"

categories_to_create = ["electronic", "jewelery", "men's clothing", "women's clothing"]

def get_token():
    resp = requests.post(LOGIN_URL, json={"email": USER_EMAIL, "password": USER_PASSWORD})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    else:
        print("Ошибка входа")
        return None

token = get_token()
if token:
    headers = {"Authorization": f"Bearer {token}"}
    for cat in categories_to_create:
        r = requests.post(CATEGORY_URL, json={"name": cat}, headers=headers)
        if r.status_code in (200, 201):
            print(f"✓ Категория '{cat}' создана")
        else:
            print(f"✗ Ошибка создания '{cat}': {r.status_code} {r.text}")