from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.db.database import Base


# Junction table for many-to-many relationship
recipe_tags = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Many-to-many relationship with Recipe
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", secondary=recipe_tags, back_populates="tags"
    )


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(100), nullable=False)

    # Many-to-many relationship with Tag
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=recipe_tags, back_populates="recipes"
    )
