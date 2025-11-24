from typing import Annotated, List, Optional
from fastapi import Depends
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship


class Instruction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    step: str
    recipe_id: int = Field(foreign_key="recipe.id")
    recipe: Optional["Recipe"] = Relationship(back_populates="instructions")


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    amount: str
    recipe_id: int = Field(foreign_key="recipe.id")
    recipe: Optional["Recipe"] = Relationship(back_populates="ingredients")


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    recipe_id: int = Field(foreign_key="recipe.id")
    recipe: Optional["Recipe"] = Relationship(back_populates="tags")


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item: str
    recipe_id: int = Field(foreign_key="recipe.id")
    recipe: Optional["Recipe"] = Relationship(back_populates="notes")


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    recipe_id: int = Field(foreign_key="recipe.id")
    recipe: Optional["Recipe"] = Relationship(back_populates="images")


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index = True)
    name: str = Field(index=True)
    description: str = ""
    instructions: List[Instruction] = Relationship(back_populates="recipe")
    ingredients: List[Ingredient] = Relationship(back_populates="recipe")
    tags: List[Tag] = Relationship(back_populates="recipe")
    notes: List[Note] = Relationship(back_populates="recipe")
    images: List[Image] = Relationship(back_populates="recipe")


# NOTE: Configuration based from fastapi example: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-models
DATABASE_URL = f"sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]