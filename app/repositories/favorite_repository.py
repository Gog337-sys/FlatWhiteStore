from sqlalchemy.orm import Session
from app.models.favorite import Favorite

class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def update(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def get_by_user_product(self, user_id: int, product_id: int) -> Favorite | None:
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id
        ).first()

    def get_all_by_user(self, user_id: int) -> list[Favorite]:
        return self.db.query(Favorite).filter(Favorite.user_id == user_id).all()

    def delete(self, favorite: Favorite) -> None:
        self.db.delete(favorite)
        self.db.commit()