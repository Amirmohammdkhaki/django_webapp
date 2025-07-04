from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Fixed typo from 'modle' to 'model'
        fields = ('username','age','email',)

class CustomUserChangeForm(UserChangeForm):  # Also fixed the class name typo (Chang -> Change)
    class Meta:
        model = CustomUser
        fields = ('username','age','email',)