from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Teacher


class TeacherForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ('email', 'first_name', 'last_name',
                  'phone_number', 'avatar', 'bio')


class TokenForm(forms.Form):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
        initial='',
        required=False)
    refresh_token = forms.CharField(max_length=500, required=False)
