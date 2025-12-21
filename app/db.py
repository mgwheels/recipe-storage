from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, relationship

from pydantic import BaseModel


Base = declarative_base()


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


# Pydantic Models (Dataclass)
class RecipeCreate(BaseModel):
    name: str
    description: str
    tags: list[str] = []  # Optional list of tag names

class RecipeResponse(BaseModel):
    id: int
    name: str
    description: str
    tags: list[str]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate_response(cls, recipe: Recipe):
        # Transform tags into strings and return the response
        return cls(
            id=recipe.id,
            name=recipe.name,
            description=recipe.description,
            tags=[tag.name for tag in recipe.tags]
        )


# Database setup
DATABASE_URL = "sqlite:///recipes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
