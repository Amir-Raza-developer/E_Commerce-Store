from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    last_name  = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    email      = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    username   = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    role       = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))
    password1  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    password2  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'username', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role', 'buyer')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter password'})
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control'}),
            'address':    forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
