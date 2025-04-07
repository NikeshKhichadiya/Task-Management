import jwt
import datetime

# Define your secret key and algorithm
SECRET_KEY = 'your_secret_key_here'  # Change this to a strong, secret key
ALGORITHM = 'HS256'

def encode_jwt(payload: dict) -> str:
    payload = payload.copy()
    # Add the expiration time to the payload (current time + 1 hour)
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=15)
    # Encode the token using the secret key and algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    # For PyJWT versions returning bytes, decode to string
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_jwt(token: str) -> dict:
    try:
        # Decode the token using the same secret key and algorithm
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        # Handle expired token
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        print("Invalid token")
        return None