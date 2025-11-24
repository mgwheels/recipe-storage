import uvicorn

from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from sqlmodel import select

from app.sql_utils import Recipe, SessionDep, create_db_and_tables, Instruction, Ingredient, Tag, Note, Image


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Recipe Storage",
    description="An API for self-hosting recipes with search functionality.",
    lifespan=lifespan
)


# Get all recipes
# TODO: Would like to enhance this to allow searching recipes
@app.get("/recipes", response_model=List[Recipe])
async def get_recipes(session: SessionDep, skip: int = 0, limit: int = 10):
    recipes = session.exec(select(Recipe).offset(skip).limit(limit)).all()
    return recipes


# Create new recipe
@app.post("/recipes", response_model=Recipe)
async def create_recipe(session: SessionDep, recipe: Recipe):
    # Preprocess recipe data
    recipe.instructions = [
        Instruction(step=instruction) for instruction in getattr(recipe, "instructions", [])
    ]
    recipe.ingredients = [
        Ingredient(name=ingredient.get("name"), amount=ingredient.get("amount"))
        for ingredient in getattr(recipe, "ingredients", [])
    ]
    recipe.tags = [Tag(name=tag) for tag in getattr(recipe, "tags", [])]
    recipe.notes = [Note(item=note) for note in getattr(recipe, "notes", [])]
    recipe.images = [Image(filename=image) for image in getattr(recipe, "images", [])]



    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe_by_id(session: SessionDep, recipe_id: int):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe not found with given id: {recipe_id}")
    return recipe


@app.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(session: SessionDep, recipe_id: int, recipe_data: Recipe):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe not found with given id: {recipe_id}")
    
    for field, value in recipe_data.model_dump().items():
        setattr(recipe, field, value)

    session.commit()
    session.refresh(recipe)
    return recipe


@app.delete("/recipes/{recipe_id}", response_model=Recipe)
async def delete_recipe(session: SessionDep, recipe_id: int):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe not found with given id: {recipe_id}")
    
    session.delete(recipe)
    session.commit()
    return recipe

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)