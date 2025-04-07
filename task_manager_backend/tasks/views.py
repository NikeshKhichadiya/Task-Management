import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import SignupSerializer, LoginSerializer, UserProfileSerializer
from token_utils import encode_jwt

class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            if not check_password(password, user.password):
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create JWT token with user information
            token_payload = {
                "user_id": user.id,
                "email": user.email
            }
            token = encode_jwt(token_payload)
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    def get(self, request, user_id):
        # Check if JWT middleware attached the token payload.
        if not hasattr(request, 'jwt_payload') or request.jwt_payload is None:
            return Response({"detail": "Unauthorized. No valid token provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Retrieve user_id from the token payload.
        token_user_id = request.jwt_payload.get("user_id")
        # Check if the user_id in the token matches the user_id in the URL.
        if token_user_id != user_id:
            return Response({"detail": "You are not authorized to view this user's data."}, status=status.HTTP_403_FORBIDDEN)
        
        # If token is valid and user IDs match, fetch the user data.
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
