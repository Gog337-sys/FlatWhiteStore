from app.database import Base, SessionLocal, engine
from app.models.product import Product
from app.repositories.product_repository import ProductRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = ProductRepository(db)

product = Product(
    price = 1500,
    size = 54,
    name = "T-shirt",
)

repository.create(product)

products = repository.get_all()

for product in products:
    print(product.id, product.price, product.size, product.name)

db.close()