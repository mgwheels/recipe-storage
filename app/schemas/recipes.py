from pydantic import BaseModel

from app.models.recipes import Recipe


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