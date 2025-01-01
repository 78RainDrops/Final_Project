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
    

class AccessRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    system_name = models.CharField(max_length=100)  # E.g., "Election System"
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.system_name}"