import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel
# Il suffit juste d'importer les models pour qu'ils soient créés dans la base
from src.api.models.recipe import Recipe


load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

sql_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
connect_args = {}


class Engine:
    def __init__(self):
        self.engine = create_engine(sql_url, echo=True, connect_args=connect_args)


    async def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
