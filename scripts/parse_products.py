import json
import random
import sys
import requests
from pathlib import Path

# ---------- НАСТРОЙКИ ----------
SAVE_LOCAL_COPY = True                # сохранить товары в data/products.json
UPLOAD_TO_API = True                  # загружать товары в магазин через API
LOCAL_JSON_OUTPUT = Path("data/products.json")

DUMMYJSON_PRODUCTS_URL = "https://dummyjson.com/products?limit=0"
DUMMYJSON_CATEGORIES_URL = "https://dummyjson.com/products/categories"

YOUR_API_URL = "http://127.0.0.1:8000/products/"
YOUR_CATEGORY_URL = "http://127.0.0.1:8000/category/"
LOGIN_URL = "http://127.0.0.1:8000/auth/login"

USER_EMAIL = "pivo@gmail.com"      # ← замените
USER_PASSWORD = "1234567890"

# ---------- ФУНКЦИИ ----------
def get_token(email: str, password: str) -> str | None:
    resp = requests.post(LOGIN_URL, json={"email": email, "password": password})
    if resp.status_code == 200:
        return resp.json().get("access_token")
    else:
        print(f"❌ Ошибка входа: {resp.status_code} {resp.text}")
        return None

def get_existing_categories(token: str) -> set[str]:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(YOUR_CATEGORY_URL, headers=headers)
        if resp.status_code == 200:
            return {cat["name"] for cat in resp.json()}
    except Exception:
        pass
    return set()

def create_category(token: str, name: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.post(YOUR_CATEGORY_URL, json={"name": name}, headers=headers)
        return resp.status_code in (200, 201)
    except:
        return False

def prepare_categories(token: str) -> dict[int, str]:
    """Получает список категорий из DummyJSON, создаёт отсутствующие, возвращает {category_id: name}."""
    resp = requests.get(DUMMYJSON_CATEGORIES_URL)
    resp.raise_for_status()
    categories_list = resp.json()  # список {"name": ..., "slug": ...}

    existing = get_existing_categories(token)
    id_to_name = {}
    for idx, cat in enumerate(categories_list, start=1):
        name = cat["name"]
        if name not in existing:
            print(f"Создаю категорию '{name}'...", end=" ")
            if create_category(token, name):
                print("✅")
                existing.add(name)
            else:
                print("❌ (пропускаем)")
        else:
            print(f"Категория '{name}' уже существует")
        id_to_name[idx] = name
    return id_to_name

def transform_product(item: dict, category_name: str) -> dict:
    price = int(float(item.get("price", 0)) * 100)
    price = max(1500, min(9999, price))
    size = random.randint(32, 60)
    return {
        "name": item["title"],
        "price": price,
        "size": size,
        "category_name": category_name,
        "image_url": item.get("thumbnail", ""),
        "description": item.get("description", "")
    }

def load_products_from_api(url: str) -> list[dict]:
    print(f"Загружаю товары из {url}...")
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("products", data)

def save_products_to_json(products: list[dict], filepath: Path) -> None:
    """Сохраняет список товаров в JSON-файл."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print(f"💾 Товары сохранены в {filepath}")

# ---------- ГЛАВНАЯ ФУНКЦИЯ ----------
def main():
    print("=== Загрузка товаров из DummyJSON ===\n")

    # 1. Получаем товары
    products = load_products_from_api(DUMMYJSON_PRODUCTS_URL)
    if not products:
        print("Нет товаров.")
        sys.exit(0)

    # 2. Сохраняем локальную копию
    if SAVE_LOCAL_COPY:
        save_products_to_json(products, LOCAL_JSON_OUTPUT)

    if not UPLOAD_TO_API:
        print("Выключена загрузка в API. Завершено.")
        return

    # 3. Авторизация и категории
    token = get_token(USER_EMAIL, USER_PASSWORD)
    if not token:
        sys.exit(1)

    print("\nПроверяю/создаю категории...")
    id_to_category = prepare_categories(token)

    # 4. Загрузка товаров
    print(f"\nЗагружаю {len(products)} товаров в магазин...")
    headers = {"Authorization": f"Bearer {token}"}
    created = 0
    skipped = 0
    for item in products:
        cat_id = item.get("category_id")
        category_name = id_to_category.get(cat_id, f"Category {cat_id}")
        product_data = transform_product(item, category_name)

        resp = requests.post(YOUR_API_URL, json=product_data, headers=headers)
        if resp.status_code in (200, 201):
            created += 1
            print(f"✅ {product_data['name']}")
        elif resp.status_code == 409:
            skipped += 1
            print(f"⏭️  {product_data['name']} (уже есть)")
        else:
            print(f"❌ Ошибка {resp.status_code} для '{product_data['name']}': {resp.text}")

    print(f"\n🎉 Готово! Загружено: {created}, пропущено: {skipped}")

if __name__ == "__main__":
    main()