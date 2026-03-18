from contextlib import asynccontextmanager


from fastapi import Depends, FastAPI
from typing import Annotated, Sequence, cast
from sqlalchemy import and_, or_, text
from sqlalchemy.sql import ColumnElement
from sqlmodel import Session, select

from src.api.database.db import Engine
from src.api.models.recipe import Recipe


engine = Engine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Création des tables si elles n'existent pas")
    await engine.create_db_and_tables()
    yield


app = FastAPI(
    title="RecipeHub API",
    description="API de gestion de recettes",
    version="0.1.0",
    lifespan=lifespan,
)

def get_session():
    with Session(engine.engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion de recettes!"}


@app.get("/recipes")
def read_recipes(session: SessionDep) -> Sequence[Recipe]:
    recipes = session.exec(select(Recipe)).all()
    return recipes


@app.get("/recipes/search")
def get_recipes_by_search_term(session:SessionDep, search_term: str | None = None, cooking_time: int | None = None) -> Sequence[Recipe]:
    filters = []

    if search_term:
        name_col = cast(ColumnElement, Recipe.name)

        filters.append(
            or_(
                name_col.ilike(f"%{search_term}%"),
                text(
                    """
                    EXISTS (
                    SELECT 1
                    FROM json_array_elements_text(recipe.ingredients) AS elem
                    WHERE elem ILIKE :search
                    )
                    """
                )
            )
        )

    if cooking_time is not None:
        filters.append(Recipe.temps_cuisson <= cooking_time)

    query = select(Recipe)

    if filters:
        query = query.where(and_(*filters))

    recipes = session.exec(query.params(search=f"%{search_term}%")).all()

    return recipes


@app.get("/recipes/{recipe_id}")
def get_recipe_by_name(search_term: str, session: SessionDep) -> Recipe | None:
    recipe = session.exec(select(Recipe).where(Recipe.name == search_term)).one()
    return recipe



@app.post("/recipes/")
def post_recipe(recipe: Recipe, session: SessionDep) -> Recipe:
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe
