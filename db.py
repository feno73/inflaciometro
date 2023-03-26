from peewee import PostgresqlDatabase

# Connect to a Postgres database.
db = PostgresqlDatabase('postgres',
                        user='postgres',
                        password='postgres',
                        host='localhost',
                        port=5432)
