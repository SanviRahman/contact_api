from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



# Create your views here.
class UserRegistration(APIView):

    permission_classes = []

    def post(self,request):

        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):

    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        user=authenticate(username=username,password=password)

        if user:
             refresh = RefreshToken.for_user(user)
             return Response(
               {
                     'message': 'You have successfully logged in',
                     'token': {
                            "refresh":str(refresh),
                            "access":str(refresh.access_token)
                            },
               },
                status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        