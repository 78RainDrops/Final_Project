from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'age', 'birthday', 'school_name', 'course', 'section', 'email', 'password1', 'password2']

class AccessRequestForm(forms.Form):
    system_name = forms.ChoiceField(choices=[
        ('Election System', 'Election System'),
        ('Alumni Network', 'Alumni Network'),
        ('Thesis Management', 'Thesis Management'),
        ('Digital Library', 'Digital Library'),
        ('Teacher Evaluation', 'Teacher Evaluation'),
    ])
