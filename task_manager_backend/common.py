from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status

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
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    
    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

def is_authenicated(token):
 
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    # if payload == None:
    #         return Response({
    #         'status': 'error',
    #         'message': 'You are not authorized to view this user data.'
    #     }, status=status.HTTP_403_FORBIDDEN)
    # else:
    #     return payload
    return payload
    