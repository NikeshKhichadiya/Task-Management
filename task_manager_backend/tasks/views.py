from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .models import User


# Sign Up View (No token required)
@api_view(['POST'])
@authentication_classes([])  # Disable authentication
@permission_classes([])  # Disable permission classes (no restrictions)
def sign_up(request):
    """
    Handle user sign-up.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create the user
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Failed to create user',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Login View (No token required)
@api_view(['POST'])
@authentication_classes([])  # Disable authentication
@permission_classes([])  # Disable permission classes (no restrictions)
def login(request):
    """
    Log in the user and generate a JWT token.
    """

    # Create the serializer to validate the login data
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():

        # Get the authenticated user from the validated data
        user = serializer.validated_data['user']
        # Generate JWT Token for the user
        access_token = AccessToken.for_user(user)

        return Response({
            'status': 'success',
            'message': 'Login successful',
            'access_token': str(access_token),
        }, status=status.HTTP_200_OK)

    return Response({
        'status': 'error',
        'message': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([]) 
@permission_classes([])
# @permission_classes([IsAuthenticated])  # Ensure that the user is authenticated using the token
def get_user_data(request, user_id):
    print(f"Authorization Header: {request.headers.get('Authorization')}")
    
    # You can also print the user
    print(f"Authenticated User: {request.user.id}")

    try:
        # Fetch the user by the provided userId
        user = User.objects.get(id=user_id)
        print(user)
        # Ensure that the `user` matches the authenticated user from the token (optional, if needed)
        if user != request.user:
            return Response({
                'status': 'error',
                'message': 'You are not authorized to view this user data.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Return the user data (can customize to return specific fields as needed)
        return Response({
            'status': 'success',
            'message': 'User data fetched successfully',
            'data': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)