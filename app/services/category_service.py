from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from app.models.category import Category
from app.repositories.categore_repositiry import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate



class CategoryService:

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create_category(self, schema: CategoryCreate) -> Category:
        category = Category(
            name=schema.name,
            description=schema.description
        )

        return self.repository.create(category)

    def get_categories(self) -> list[Category]:
        return self.repository.get_all()

    def get_category(self, category_id: int) -> Category:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return category

    def update_category(self, category_id: int, schema: CategoryUpdate) -> Category:
        category = self.get_category(category_id)

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided"
            )

        for field, value in update_data.items():
            setattr(category, field, value)

        return self.repository.update(category)

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)

        self.repository.delete(category)