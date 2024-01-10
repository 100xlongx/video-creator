from peewee import PostgresqlDatabase
import os

def get_database():
    return PostgresqlDatabase(
        os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

db = get_database()