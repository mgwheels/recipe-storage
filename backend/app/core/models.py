from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipes.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationship to Recipe
    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipes.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationship to Recipe
    recipe: Mapped["Recipe"] = relationship(back_populates="tags")


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=""
    )
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True, default="")

    # One-to-many relationship with Ingredient
    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient", back_populates="recipe", cascade="all, delete-orphan"
    )
    # One-to-many relationship with Tag
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", back_populates="recipe", cascade="all, delete-orphan"
    )
