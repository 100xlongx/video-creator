from dotenv import load_dotenv
load_dotenv()

import os
import secrets
import string
import random
import hashlib
import base64
from urllib.parse import urlencode

# from db.connection import create_connection
# from db.models import OAuthTokens

# db = create_connection()

# auth_token = OAuthTokens.get(OAuthTokens.id == 4)

# print(auth_token)

def generate_code_verifier(length=128):
    characters = string.ascii_letters + string.digits + "-._~"
    return ''.join(random.choice(characters) for _ in range(length))

def generate_code_challenge(code_verifier):
    sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(sha256_hash).decode().rstrip("=")
# db.close()

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
state_token = secrets.token_urlsafe(16)
redirect = "https://localhost:8000/callback"

query_params = {
    'client_key': os.getenv('TIKTOK_CLIENT_KEY'),
    'redirect_uri': redirect,
    'scope': os.getenv('TIKTOK_SCOPES'),
    'state': state_token,
    'response_type': 'code',
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256'
}

encoded_query_params = urlencode(query_params)

auth_page = f"https://www.tiktok.com/v2/auth/authorize?{encoded_query_params}"

print(auth_page)