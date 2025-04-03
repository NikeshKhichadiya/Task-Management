from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password,make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is not included in the response

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)  # Hash the password
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the email and password combination.
        """
        email = data.get('email')
        password = data.get('password')

        try:
            # Query the user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        # Check if the password matches
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user  # Store the authenticated user in the data
        return data
    

class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']  