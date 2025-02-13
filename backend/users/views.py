from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import *
# from utils.function import *
from django.contrib.auth import get_user_model
from users.models import *
from django.conf import settings
import re
User = get_user_model()
# Create your views here.


def get_auth_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'user':UserLoginSerializer(user).data,
        # 'permission':get_all_user_permissions(user),
        'refresh': str(refresh),
        'token': str(refresh.access_token) 
    }
    
    
class SignInAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CodeEmailSerializer
    def post(self, request,*args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            email = serializers.data["email"]
            password = serializers.data["password"]
            if User.objects.filter(email=email): 
                user = authenticate(email=email,password=password)
                if not user:
                    response_data = {'message':'Invalid Credential'}
                    return Response(response_data, status=400)
                
                user_data = get_auth_for_user(user)
                return Response(user_data, status=200)
            else:
                return Response(
                    {
                        "status": "error",
                        "detail": "User Not Found",
                    },
                    status=404,
                )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
class RegistrationAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    def post(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            name = serializer.validated_data["name"]
            user_type = serializer.validated_data["user_type"]
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return Response(
                    {"status": "failure", "detail": "Invalid email address format"},
                    status=400,
                )
            
            user = User.objects.create_user(username=email, email=email, password=password,name=name,user_type=user_type)
            user.save()
            user_data = get_auth_for_user(user)
            return Response(user_data, status=200) 
            
        else:
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
class GetAllDoctorsAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    required_permissions = [ "setup.view_institution"]

    serializer_class = UserRegistrationSerializer

    def get(self, request,*args, **kwargs):
        doctors = User.objects.filter(user_type="Doctor").all()
        serializers = self.serializer_class(doctors,many=True)
        return Response(
            {"status": "success", "success_message": serializers.data},
            status=200
        )       