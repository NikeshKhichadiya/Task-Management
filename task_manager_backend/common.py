from django.contrib.auth.hashers import make_password, check_password

def hash_password(password: str) -> str:
    """
    Hashes the given password and returns only the hashed part.
    
    :param password: The password to hash.
    :return: The hashed password without the PBKDF2, iterations, and salt.
    """
    # Hash the password using Django's make_password() method
    hashed_password = make_password(password)
    
    # Return only the hashed password
    return hashed_password

def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verifies a password by comparing it with the stored hashed password.
    
    :param stored_hash: The stored hashed password (without PBKDF2, iterations, and salt).
    :param password: The password to verify.
    :return: True if the password matches, False otherwise.
    """
    # Since we are storing only the hashed password, we manually check it
    return check_password(password, stored_hash)

import jwt
import datetime

# Secret key for encoding and decoding the JWT
SECRET_KEY = 'your_secret_key_here'

def generate_token(user_id):
    """
    Generates a JWT token valid for 15 minutes.

    Args:
    - user_id (str): The user identifier, typically the user's ID or email.

    Returns:
    - str: The JWT token.
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    
    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

def decode_token(token):
    """
    Decodes the JWT token and returns the payload if valid.

    Args:
    - token (str): The JWT token.

    Returns:
    - dict: The payload data if the token is valid.
    - None: If the token is expired or invalid.
    """
    try:
        # Decode the token and verify expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None