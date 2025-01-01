from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    birthday = models.DateField()
    school_name = models.CharField(max_length=255)
    course = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username