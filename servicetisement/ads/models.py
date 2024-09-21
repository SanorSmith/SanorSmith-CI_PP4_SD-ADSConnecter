from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    occupation = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
