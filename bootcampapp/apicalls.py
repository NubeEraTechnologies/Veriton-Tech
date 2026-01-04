import requests
from datetime import datetime, timedelta
access_token = None
expires_at = None
def fetch_new_token( username, password):
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
        expires_in = timedelta(minutes=9)  # Expiration buffer
        expires_at = datetime.now() + expires_in
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token: {e}")
        return None

def get_token( username, password):
    if access_token is None or datetime.now() >= expires_at:
        return fetch_new_token(username, password)
    return access_token
    

from bootcampapp.encryption_utils import decrypt_password
from django.http import JsonResponse

def get_user_auth(request):
    username = request.user.username
    encrypted_password = request.session.get('yono')
    if not encrypted_password:
        return None, JsonResponse({"error": "User not validated"}, status=401)

    # Decrypt the password
    password = decrypt_password(encrypted_password)
    return username, password

def make_api_request(api_url, token, method="GET", data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        if method == "POST":
            response = requests.post(api_url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(api_url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(api_url, headers=headers)
        else:  # Default is GET
            response = requests.get(api_url, headers=headers)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return {"error": "Request failed"}   

    
def handle_api_request(request, section, method="GET", data=None, object_id=None):
    """
    Handles API requests for different HTTP methods.
    """
    api_url = f"http://127.0.0.1:786/api/{section}/"
    if object_id:  # Include object ID in the URL for update or delete
        api_url += f"{object_id}/"

    username, password = get_user_auth(request)
    if username is None:
        return {"error": "Unable to authenticate user"}

    token = get_token(username, password)
    if token is None:
        return {"error": "Unable to obtain token"}

    # Make the API request with the appropriate method
    return make_api_request(api_url, token, method=method, data=data)

def fetch_data(request, section):
    return handle_api_request(request, section, method="GET")

def create_data(request, section, data):
    return handle_api_request(request, section, method="POST", data=data)

def update_data(request, section, object_id, data):
    return handle_api_request(request, section, method="PUT", object_id=object_id, data=data)

def delete_data(request, section, object_id):
    return handle_api_request(request, section, method="DELETE", object_id=object_id)
