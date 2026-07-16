from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    name = Column(String, nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    image_url = Column(String, nullable=True)          # ← ДОБАВЬТЕ ЭТУ СТРОКУ

    category = relationship("Category", back_populates="products")
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")