import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from decouple import config
import base64
import requests

def validate_jwt_token(token):
    try:
        secret_key = base64.b64decode(config("TWITCH_EXTENSION_SECRET"))
        # Decode the token
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")
    

def get_twitch_access_token():
    client_id =config("TWITCH_APP_ID")
    client_secret = config("TWITCH_APP_SECRET")

    res = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    })
    
    return res.json()["access_token"]
    