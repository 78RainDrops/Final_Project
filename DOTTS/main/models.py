# models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=User )
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User )
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
#     # Add any additional fields you need
#     bio = models.TextField(blank=True, null=True) 

class AccessRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    system_name = models.CharField(max_length=100)  # E.g., "Election System"
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.system_name}"