from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models.recipes import Recipe, Tag
from app.schemas.recipes import RecipeCreate, RecipeResponse
from app.services.receipes_service import process_tags

router = APIRouter(prefix="/recipes", tags=["recipes"])


# Read all recipes
@router.get(
    "/",
    description="Get all recipes from database",
    response_model=List[RecipeResponse],
)
def get_recipes(session: Session = Depends(get_db)):
    # Query all recipes
    recipes = session.query(Recipe).all()

    return [RecipeResponse.model_validate_response(recipe) for recipe in recipes]


# Create recipe
@router.post(
    "/",
    description="Create new recipe and add to database",
    response_model=RecipeResponse,
)
def create_recipe(recipe: RecipeCreate, session: Session = Depends(get_db)):
    if session.query(Recipe).filter(Recipe.name == recipe.name).first():
        raise HTTPException(status_code=404, detail="Recipe already exists!")

    # Create new recipe
    new_recipe = Recipe(name=recipe.name, description=recipe.description)
    session.add(new_recipe)

    # Process tags
    process_tags(recipe, new_recipe, session)

    session.commit()
    session.refresh(new_recipe)

    return RecipeResponse.model_validate_response(new_recipe)


# Read recipe by ID
# TODO: add description
@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(recipe_id: int, session: Session = Depends(get_db)):
    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found!")

    return RecipeResponse.model_validate_response(recipe)


# Update recipe by ID
# TODO: add description
@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int, recipe: RecipeCreate, session: Session = Depends(get_db)
):
    db_recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe does not exist!")

    # Update recipe fields
    db_recipe.name = recipe.name
    db_recipe.description = recipe.description

    # Update tags
    db_recipe.tags.clear()  # Remove existing tags
    process_tags(recipe, db_recipe, session)

    session.commit()
    session.refresh(db_recipe)

    return RecipeResponse.model_validate_response(db_recipe)


# Delete recipe by ID
# TODO: add description
@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, session: Session = Depends(get_db)):
    db_recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe does not exist!")

    session.delete(db_recipe)
    session.commit()
    return {"message": "Recipe deleted!"}


# Read recipes by tag
@router.get(
    "/tags/{tag_name}",
    description="Search recipes by tag",
    response_model=List[RecipeResponse],
)
def search_recipes_by_tag(tag_name: str, session: Session = Depends(get_db)):
    # Query recipes that have the given tag
    recipes = session.query(Recipe).join(Recipe.tags).filter(Tag.name == tag_name).all()

    return [RecipeResponse.model_validate_response(recipe) for recipe in recipes]
