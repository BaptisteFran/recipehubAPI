from fastapi import FastAPI

app = FastAPI(
    title="RecipeHub API",
    description="API de gestion de recettes",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion de recettes!"}


@app.get("/recipes")
def read_recipes():
    return {"recipes": []}


@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int):
    return {"recipe_id": recipe_id}
