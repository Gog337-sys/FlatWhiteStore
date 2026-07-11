from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    favorited_by = relationship("Favorite", back_populates="product")