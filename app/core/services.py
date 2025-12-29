from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.models import Recipe, Tag
from app.core.schemas import RecipeCreate


# TODO: Docstring
def process_tags(recipe: RecipeCreate, db_recipe: Recipe, session: Session) -> None:
    # Process tags
    for tag_name in recipe.tags:
        tag_name = tag_name.lower()
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            # Create a new tag if it doesn't exist
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()
            session.refresh(tag)
        # Associate the tag with the recipe
        db_recipe.tags.append(tag)


# TODO: Docstring
def assign_recipe(recipe: RecipeCreate, db_recipe: Recipe) -> None:
    if recipe.name:
        db_recipe.name = recipe.name
    if recipe.description:
        db_recipe.description = recipe.description
    if recipe.notes:
        db_recipe.notes = recipe.notes


# TODO: Docstring
def get_recipe_by_id_handler(recipe_id: int, session: Session) -> Recipe | None:
    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=404, detail=f"Recipe not found for id: {recipe_id}"
        )
    return recipe
