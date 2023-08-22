from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    country = models.CharField(max_length=100, verbose_name='country', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='phone', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class VerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
