import os

from dotenv import load_dotenv
from peewee import PostgresqlDatabase

load_dotenv()

# Connect to a Postgres database.
db = PostgresqlDatabase('postgres',
                        user='postgres',
                        password='postgres',
                        host=os.getenv("DB_HOST"),
                        port=5432)
