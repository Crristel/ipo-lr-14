from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm # для аутентификации последняя
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','about_yourself')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','about_yourself')


class Filter(forms.Form):
    category = forms.CharField(required=False, label='Категория')
    maker = forms.CharField(required=False,label='Производитель')
    search = forms.CharField(required=False)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name','about_yourself','email','password1','password2')

class LoginForm(AuthenticationForm):
    pass