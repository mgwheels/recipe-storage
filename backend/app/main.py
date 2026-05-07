from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.routers import router as recipes_router
from app.core.database import Base, Engine

Base.metadata.create_all(Engine)

app = FastAPI(
    title="Recipe Storage",
    description="A recipes API with search functionality, using fastapi and sqlalchemy.",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(recipes_router)


@app.get("/")
def root():
    return {"message": "Recipe Storage API Running"}
