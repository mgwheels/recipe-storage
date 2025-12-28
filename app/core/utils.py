from sqlalchemy.orm import Session

from app.core.models import Recipe, Tag
from app.core.schemas import RecipeCreate


# TODO: Docstring
def process_tags(recipe: RecipeCreate, db_recipe: Recipe, session: Session):
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
