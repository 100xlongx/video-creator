import json
import time

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

def save_token_with_timestamp(token_response, file_path='tiktok_tokens.json'):
    current_time = int(time.time())  # Current time in seconds since the Epoch
    token_data = {
        'access_token': token_response.get('access_token'),
        'refresh_token': token_response.get('refresh_token'),
        'expires_in': token_response.get('expires_in'),
        'obtained_at': current_time,  # Timestamp of when the token was obtained
        'refresh_expires_in': token_response.get('refresh_expires_in')
    }

    with open(file_path, 'w') as file:
        json.dump(token_data, file, indent=4)

# Example Usage:
# tokens = read_tokens()
# tokens['account1'] = {'access_token': 'new_access_token', 'refresh_token': 'new_refresh_token'}
# write_tokens(tokens)

# is_token_expired usage
# if is_token_expired():
#     refresh_token()