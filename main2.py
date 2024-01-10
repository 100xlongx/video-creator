from dotenv import load_dotenv
load_dotenv()

from db.connection import create_connection
from db.models import OAuthTokens

connection = create_connection()

auth_token = OAuthTokens.get(OAuthTokens.id == 4)

print(f"ID: {auth_token.id}")
print(f"User ID: {auth_token.user_id}")
print(f"Provider: {auth_token.provider}")
print(f"Access Token: {auth_token.access_token}")
print(f"Refresh Token: {auth_token.refresh_token}")
print(f"Expires At: {auth_token.expires_at}")
print(f"Scopes: {auth_token.scopes}")
print(f"Created At: {auth_token.created_at}")
print(f"Updated At: {auth_token.updated_at}")