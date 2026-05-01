from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import joinedload, Session
from typing import List

from app.core.database import get_db
from app.core.models import Recipe
from app.core.schemas import RecipeCreate, RecipeResponse
from app.core.services import (
    process_tags,
    process_ingredients,
    get_recipe_by_id_handler,
)

router = APIRouter(prefix="/recipes", tags=["recipes"])


# Read all recipes
@router.get(
    "/",
    description="Get all recipes from database",
    response_model=List[RecipeResponse],
)
def get_recipes(session: Session = Depends(get_db)):
    recipes = session.query(Recipe).options(
        joinedload(Recipe.tags),
        joinedload(Recipe.ingredients)
    ).all()
    return [RecipeResponse.model_validate_response(recipe) for recipe in recipes]



# Create recipe
@router.post(
    "/",
    description="Create new recipe and add to database",
    response_model=RecipeResponse,
)
def create_recipe(recipe: RecipeCreate, session: Session = Depends(get_db)):
    if session.query(Recipe).filter(Recipe.name == recipe.name).first():
        raise HTTPException(status_code=409, detail="Recipe already exists!")

    # Create new recipe
    new_recipe = Recipe(name=recipe.name)
    new_recipe.description = recipe.description
    new_recipe.notes = recipe.notes
    session.add(new_recipe)

    # Process tags
    process_tags(recipe, new_recipe)

    # Process ingredients
    process_ingredients(recipe, new_recipe)

    session.commit()
    session.refresh(new_recipe)

    return RecipeResponse.model_validate_response(new_recipe)


# Read recipe by ID
@router.get(
    "/{recipe_id}",
    description="Get recipe by ID from database",
    response_model=RecipeResponse,
)
def get_recipe_by_id(recipe_id: int, session: Session = Depends(get_db)):
    recipe = get_recipe_by_id_handler(recipe_id, session)
    return RecipeResponse.model_validate_response(recipe)


# Update recipe by ID
@router.put(
    "/{recipe_id}",
    description="Update recipe in database by ID",
    response_model=RecipeResponse,
)
def update_recipe(
    recipe_id: int, recipe: RecipeCreate, session: Session = Depends(get_db)
):
    db_recipe = get_recipe_by_id_handler(recipe_id, session)

    # Update recipe fields directly
    db_recipe.name = recipe.name
    db_recipe.description = recipe.description
    db_recipe.notes = recipe.notes

    # Update tags
    process_tags(recipe, db_recipe)

    # Update ingredients
    process_ingredients(recipe, db_recipe)

    session.commit()
    session.refresh(db_recipe)

    return RecipeResponse.model_validate_response(db_recipe)


# Delete recipe by ID
@router.delete(
    "/{recipe_id}",
    description="Delete recipe by ID from database",
)
def delete_recipe(recipe_id: int, session: Session = Depends(get_db)):
    db_recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe does not exist!")

    session.delete(db_recipe)
    session.commit()
    return {"message": "Recipe deleted!"}

