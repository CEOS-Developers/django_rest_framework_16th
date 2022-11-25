from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label='email', required=True, widget=forms.EmailInput)
    nickname = forms.CharField(label='nickname', required=False, widget=forms.TextInput)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]
