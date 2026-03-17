import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

sql_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
connect_args = {}


engine = create_engine(sql_url, echo=True, connect_args=connect_args)


async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
