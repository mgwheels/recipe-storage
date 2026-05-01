from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict

from app.core.models import Recipe


# Pydantic Models (Dataclass)
class RecipeCreate(BaseModel):
    name: str = ""
    description: str = ""
    ingredients: list[dict[str, str]] = [{"name": "", "quantity": ""}]
    notes: str = ""
    tags: list[str] = [""]


class RecipeResponse(BaseModel):
    id: int
    name: str
    description: str = ""
    ingredients: list[dict[str, str]] = []
    notes: str = ""
    tags: list[str] = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate_response(cls, recipe: Recipe):
        try:
            return cls(
                id=recipe.id,
                name=recipe.name,
                description=recipe.description or "",
                ingredients=[{"name": ing.name, "quantity": ing.quantity or ""} for ing in recipe.ingredients],
                notes=recipe.notes or "",
                tags=[tag.name for tag in recipe.tags],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error building response: {e}")
