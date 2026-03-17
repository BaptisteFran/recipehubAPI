from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Recipe(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(
        index=True
    )  # Mettre des index pour optimiser les recherches dans la db
    ingredients: list = Field(sa_column=Field(default="[]", sa_column_kwargs={"type_": "TEXT"}))