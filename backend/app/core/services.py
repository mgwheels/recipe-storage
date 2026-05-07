from fastapi import HTTPException
from sqlalchemy.orm import joinedload, Session

from app.core.models import Recipe, Tag, Ingredient
from app.core.schemas import RecipeCreate


# TODO: Docstring
def process_tags(recipe: RecipeCreate, db_recipe: Recipe) -> None:
    # Clear existing tags
    db_recipe.tags.clear()

    # Add new tags, skipping empty/whitespace-only entries
    for tag_name in recipe.tags:
        cleaned_tag = tag_name.strip().lower()
        if not cleaned_tag:
            continue

        # Create and append tag
        tag = Tag(name=cleaned_tag)
        db_recipe.tags.append(tag)


# TODO: Docstring
def process_ingredients(recipe: RecipeCreate, db_recipe: Recipe) -> None:
    # Clear existing ingredients
    db_recipe.ingredients.clear()

    # Add new ingredients, skipping empty names
    for ingredient_data in recipe.ingredients:
        ingredient_name = ingredient_data.get("name", "").strip().lower()
        if not ingredient_name:
            continue
        ingredient_quantity = ingredient_data.get("quantity", "").strip()

        # Create and append ingredient
        ingredient = Ingredient(name=ingredient_name, quantity=ingredient_quantity)
        db_recipe.ingredients.append(ingredient)


# TODO: Docstring
def get_recipe_by_id_handler(recipe_id: int, session: Session) -> Recipe:
    recipe = (
        session.query(Recipe)
        .options(joinedload(Recipe.tags), joinedload(Recipe.ingredients))
        .filter(Recipe.id == recipe_id)
        .first()
    )
    if not recipe:
        raise HTTPException(
            status_code=404, detail=f"Recipe not found for id: {recipe_id}"
        )
    return recipe
