import requests

def get_auth_token(x_token: str) -> bool:
    valid_token = requests.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={x_token}")
    return valid_token.status_code == 200
