from dotenv import load_dotenv
load_dotenv()

from db.database import db
from db.models import OAuthTokens

# Connect to the database and create tables if they don't exist
db.connect()
db.create_tables([OAuthTokens], safe=True)