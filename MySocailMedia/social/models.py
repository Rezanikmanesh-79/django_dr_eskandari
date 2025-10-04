from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='account_image/', null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    date_of_join = models.DateField(auto_now_add=True)
