import os
from peewee import PostgresqlDatabase
from dotenv import load_dotenv

load_dotenv()

# Connect to a Postgres database.
db = PostgresqlDatabase('postgres',
                        user='postgres',
                        password='postgres',
                        host=os.getenv("DB_HOST"),
                        port=5432)
