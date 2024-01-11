from dotenv import load_dotenv
load_dotenv()

from db.connection import create_connection
from db.models import OAuthTokens

db = create_connection()

auth_token = OAuthTokens.get(OAuthTokens.id == 4)

print(auth_token)

db.close()