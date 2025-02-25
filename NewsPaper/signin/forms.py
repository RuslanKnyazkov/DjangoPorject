from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django import forms
from .models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class BaseUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'firstname', 'lastname', 'bio', 'birth_date']

        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'birth_date' : forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio' : forms.Textarea(attrs={'class': 'form-control'})
        }


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={
                'class': 'form-control'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={
                'class': 'form-control'}))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ["username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите Логин'
            }),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
        }
