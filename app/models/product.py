from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)


    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.id"),
        nullable=True,
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")