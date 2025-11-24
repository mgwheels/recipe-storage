import uuid

class Recipe:
    def __init__(
            self,
            name: str,
            description: str,
            ingredients: list[dict[str, str]] = [],
            instructions: list[str] = [],
            tags: list[str] = [],
            notes: list[str] = [],
            imgs: list[str] = []
            ):
        self.id: str = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.tags = tags
        self.notes = notes
        self.imgs = imgs
