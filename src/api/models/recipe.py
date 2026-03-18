from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Recipe(SQLModel, table=True):
    """
    Modèle de données pour une recette, utilisant SQLModel pour la gestion de la base de données. Chaque champ correspond à une colonne dans la table "recipe" de la base de données. Les types de données sont définis pour chaque champ, et des propriétés supplémentaires sont ajoutées pour optimiser les recherches et garantir l'intégrité des données.
    Une recette doit avoir :
        - un nom
        - une catégorie
        - une description (optionnel)
        - des étapes de préparation (optionnel)
        - des images de la recette (optionnel)
        - des ingrédients (optionnel)
        - un temps de cuisson (optionnel)
    """

    # On rajoute Field, pour pouvoir donner des propriétés à nos champs, comme les index, les clés primaires, etc.
    id: int = Field(default=None, primary_key=True)
    name: str = Field(
        index=True,
        nullable=False,
    )  # Mettre des index pour optimiser les recherches dans la db
    slug_name: str
    category: str = Field(index=True)
    description: str = Field(max_length=255)
    preparation_steps: str = Field(nullable=True, max_length=1000)
    recipe_images: list = Field(default_factory=list, sa_column=Column(JSON))
    ingredients: list = Field(default_factory=list, sa_column=Column(JSON))
    temps_cuisson: int = Field(
        index=True,
        nullable=False,
    )  # Mettre des index pour optimiser les recherches dans la db
