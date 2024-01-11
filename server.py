import http.server
import socketserver
import urllib.parse as urlparse
import requests
import os
from dotenv import load_dotenv
from tiktok_utils import save_token_with_timestamp

load_dotenv()

PORT = 8000
CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8000/callback'  # This should match the redirect URI registered with TikTok

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Extract the authorization code from the URL
        query_components = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        code = query_components.get('code', None)

        if code:
            code = code[0]  # Extract the first code value
            # Exchange the code for a token
            token_response = self.exchange_code_for_token(code)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if 'access_token' in token_response:
                self.wfile.write(b"Token received successfully. You can close this window.")
                save_token_with_timestamp(token_response) # Save the token to a file
            else:
                self.wfile.write(b"Failed to receive token.")
        else:
            self.send_error(400, "No code found in the request")

    def exchange_code_for_token(self, code):
        payload = {
            'client_key': CLIENT_KEY,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
        response = requests.post('https://open.tiktokapis.com/v2/oauth/token/', data=payload)
        return response.json()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
