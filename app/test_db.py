from app.database import engine
from app.models.product import Product
from app.models.category import Category
from app.database import Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables created")