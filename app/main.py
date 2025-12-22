from fastapi import FastAPI

from app.routers.recipes import router as recipes_router


app = FastAPI(
    title="Recipe Storage",
    description="A recipes API with search functionality, using fastapi and sqlalchemy.",
)

app.include_router(recipes_router)


@app.get("/")
def root():
    return {"message": "Recipe Storage API Running"}
