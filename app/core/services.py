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
