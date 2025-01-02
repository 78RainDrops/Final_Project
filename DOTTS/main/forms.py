from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import UserProfile
from datetime import date

class CustomSelectDateWidget(forms.SelectDateWidget):
    def __init__(self, years=None, *args, **kwargs):
        if years is None:
            # Set the default range of years (e.g., from 1900 to 2025)
            years = range(1900, 2026)
        super().__init__(years=years, *args, **kwargs)

    def get_context(self, name, value, attrs):
        # Get the current year
        current_year = date.today().year
        # Set the initial value for the year dropdown to the current year
        if value is None:
            value = date.today()  # Set to today's date if no value is provided
        return super().get_context(name, value, attrs)

def validate_min_year(value):
    if value < date(2025, 1, 1):
        raise ValidationError(
            _('The date must be on or after January 1, 2025.'),
            params={'value': value},
        )

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)  # Add email field
    first_name = forms.CharField(max_length=30, required=False)  # Add first name field
    last_name = forms.CharField(max_length=30, required=False)  # Add last name field
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    age = forms.IntegerField()
    birthday = forms.DateField(widget=CustomSelectDateWidget())
    school_name = forms.CharField(max_length=100)
    course = forms.CharField(max_length=100)
    section = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'age', 'birthday', 'school_name', 'course', 'section']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Validate the password using Django's built-in validators
        if password:
            validate_password(password)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']  # Set the email
        user.first_name = self.cleaned_data['first_name']  # Set the first name
        user.last_name = self.cleaned_data['last_name']  # Set the last name
        if commit:
            user.save()
            profile = UserProfile(
                user=user,
                age=self.cleaned_data['age'],
                birthday=self.cleaned_data['birthday'],
                school_name=self.cleaned_data['school_name'],
                course=self.cleaned_data['course'],
                section=self.cleaned_data['section']
            )
            profile.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
# from .models import UserProfile

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['age', 'birthday', 'school_name', 'course', 'section']
#         widgets = {
#             'birthday': forms.DateInput(attrs={'type': 'date'}),
#         }

# class UserLoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
        
# # class UserLoginForm(AuthenticationForm):
# #     class Meta:
# #         model = CustomUser 
# #         fields = ['username', 'password']

# # class CustomAuthenticationForm(AuthenticationForm):
# #     pass  # Use the default Django AuthenticationForm