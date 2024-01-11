import json
import time
import datetime

from db.models import OAuthTokens

def read_tokens(file_path='tiktok_tokens.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_tokens(data, file_path='tiktok_tokens.json'):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def is_token_expired(file_path='tiktok_tokens.json'):
    with open(file_path, 'r') as file:
        token_data = json.load(file)
        current_time = int(time.time())
        # Calculate when the token is set to expire
        expiry_time = token_data['obtained_at'] + token_data['expires_in']
        return current_time >= expiry_time

def save_token_with_timestamp(token_response):
    access_token = token_response['access_token']
    refresh_token = token_response.get('refresh_token', None) # Not all providers return a refresh token
    expires_in = token_response['expires_in'] # Duration in seconds

    expires_at = datetime.now() + datetime.timedelta(seconds=expires_in)

    # Create a new token record
    new_token = OAuthTokens.create(
        user_id='bot1',  # You need to determine how to set this
        provider='tiktok',
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at
    )

    # Save the record to the database
    new_token.save()

    print(new_token)



    # current_time = int(time.time())  # Current time in seconds since the Epoch
    # token_data = {
    #     'access_token': token_response.get('access_token'),
    #     'refresh_token': token_response.get('refresh_token'),
    #     'expires_in': token_response.get('expires_in'),
    #     'obtained_at': current_time,  # Timestamp of when the token was obtained
    #     'refresh_expires_in': token_response.get('refresh_expires_in')
    # }

    # with open(file_path, 'w') as file:
    #     json.dump(token_data, file, indent=4)

# Example Usage:
# tokens = read_tokens()
# tokens['account1'] = {'access_token': 'new_access_token', 'refresh_token': 'new_refresh_token'}
# write_tokens(tokens)

# is_token_expired usage
# if is_token_expired():
#     refresh_token()