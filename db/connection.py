from db.database import db
from db.models import OAuthTokens

def create_connection():
    # Connect to the database and create tables if they don't exist
    db.connect()
    db.create_tables([OAuthTokens], safe=True)