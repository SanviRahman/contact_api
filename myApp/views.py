from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserRegistration(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and hash the password
            user = serializer.save()
            return Response(
                {
                    'message': 'User registered successfully',
                    'user_id': user.id,
                    'username': user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response(
                {'message': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # Check if the user is active
            if not user.is_active:
                return Response(
                    {'message': 'User account is not active'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'message': 'You have successfully logged in',
                    'token': {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )