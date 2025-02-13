from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import *
User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'user_type'
        ]
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'name',
            'user_type'
        ]
        extra_kwargs = {'password': {'write_only': True}}
        
    # def create(self, validated_data):
    #     # CLEAN ALL VALUES
    #     email_address = validated_data['email_address'].lower()
    #     password = validated_data['password']
    #     # CREATE A NEW  USER
    #     user = User.objects.create(
    #         username=email_address,
    #         email_address=email_address,
    #     )
    #     user.set_password(password)
    #     user.save()
    #     return user


class CodeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=254)

