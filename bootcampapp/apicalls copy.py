import requests
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta
from bootcampapp.encryption_utils import decrypt_password

# Global storage for token and expiry
TOKEN_INFO = {
    "access_token": None,
    "expires_at": None
}

# Function to fetch a new token using current user credentials
def fetch_new_token(username, password):
    api_url = "http://127.0.0.1:786/api/token/"  # Your token generation endpoint
    credentials = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(api_url, data=credentials)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access")
        expires_in = timedelta(minutes=9)  # Set a safe expiration buffer
        TOKEN_INFO["access_token"] = access_token
        TOKEN_INFO["expires_at"] = datetime.now() + expires_in
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token: {e}")
        return None

# Get or refresh token
def get_token(username, password):
    if TOKEN_INFO["access_token"] is None or datetime.now() >= TOKEN_INFO["expires_at"]:
        return fetch_new_token(username, password)
    return TOKEN_INFO["access_token"]

def getuserauth(request):
    username = request.user.username
    encrypted_password = request.session.get('password')
    if not encrypted_password:
        return JsonResponse({"error": "user not validated"})

    # Decrypt the password
    password = decrypt_password(encrypted_password)
    return username, password
# Fetch API data
def getapilist(request,section):
    api_url = f"http://127.0.0.1:786/api/{section}/"
    username, password = getuserauth(request)
    token = get_token(username, password)  # Get the current token
    if token is None:
        return {"error": "Unable to obtain token"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return {"error": "Unable to fetch data"}

  