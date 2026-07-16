import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.category import Category
from app.models.product import Product        # обязательно
from app.models.user import User              # обязательно для Favorite
from app.models.favorite import Favorite      # обязательно
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.services.product_service import ProductService

JSON_FILE = Path("data/products.json")

def read_json(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get("products", data.get("data", []))

def ensure_categories(session, products: list[dict]) -> dict[int, str]:
    unique_ids = {item.get("category_id") for item in products if "category_id" in item}
    existing_categories = {
        cat.name: cat for cat in session.query(Category).all()
    }
    id_to_name = {}

    for cat_id in sorted(unique_ids):
        desired_name = f"Category {cat_id}"
        if desired_name not in existing_categories:
            new_cat = Category(name=desired_name)
            session.add(new_cat)
            session.flush()
            existing_categories[desired_name] = new_cat
            print(f"  + Создана категория: {desired_name}")
        else:
            print(f"  Категория '{desired_name}' уже существует")
        id_to_name[cat_id] = desired_name

    return id_to_name

def import_products() -> None:
    products_data = read_json(JSON_FILE)
    if not products_data:
        print("Файл пуст или не содержит товаров.")
        return

    created_count = 0
    error_count = 0
    skipped_count = 0

    with SessionLocal() as session:
        print("Проверка/создание категорий...")
        id_to_category = ensure_categories(session, products_data)

        repository = ProductRepository(session)
        service = ProductService(session)

        for item in products_data:
            try:
                cat_id = item.get("category_id")
                if cat_id is not None:
                    category_name = id_to_category.get(cat_id, f"Category {cat_id}")
                else:
                    category_name = "Без категории"
                    if category_name not in {c.name for c in session.query(Category).all()}:
                        session.add(Category(name=category_name))
                        session.flush()

                raw_price = float(item.get("price", 0))
                price = int(raw_price * 100)
                price = max(1500, min(9999, price))

                if "size" in item:
                    size = int(item["size"])
                else:
                    import random
                    size = random.randint(32, 60)

                product_schema = ProductCreate(
                    name=item["title"],
                    price=price,
                    size=size,
                    category_name=category_name,
                    image_url=item.get("thumbnail") or item.get("image_url", ""),
                    description=item.get("description", ""),
                )

                service.create_product(product_schema, current_user=None)
                created_count += 1
                print(f"  ✓ {product_schema.name}")

            except Exception as error:
                if "already exists" in str(error).lower() or "unique constraint" in str(error).lower():
                    skipped_count += 1
                    print(f"  ⏭️  {item.get('title', '?')} уже существует, пропущено")
                else:
                    error_count += 1
                    print(f"  ✗ Ошибка для '{item.get('title', '?')}': {error}")

        session.commit()

    print(f"\nГотово: добавлено {created_count}, пропущено дубликатов {skipped_count}, ошибок {error_count}")

if __name__ == "__main__":
    import_products()