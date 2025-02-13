import uuid
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from cryptography.fernet import Fernet
from users.managers import CustomUserManager

# Generate a secret key for encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
cipher = Fernet(ENCRYPTION_KEY.encode())

class User(AbstractUser):
    USER_TYPES = (
        ("Doctor", "Doctor"),
        ("Patient", "Patient"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email