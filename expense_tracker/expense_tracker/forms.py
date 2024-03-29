from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from .models import *
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class UpdateProfileForm(forms.ModelForm):
    day_limit = forms.IntegerField(label='Ежедневный лимит', widget=forms.NumberInput(attrs={'min': 0}))
    week_limit = forms.IntegerField(label='Еженедельный лимит', widget=forms.NumberInput(attrs={'min': 0}))
    month_limit = forms.IntegerField(label='Еженедельный лимит', widget=forms.NumberInput(attrs={'min': 0}))

    class Meta:
        model = Profile
        fields = [
            'day_limit',
            'week_limit',
            'month_limit'
        ]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'type': 'password'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'type': 'password'}))
    new_password2 = forms.CharField(label='Введите пароль повторно',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class AddExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        self.fields['category'].queryset = Category.objects.filter(user=self.request.user)

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'date']
        widgets = {
            'name': forms.TextInput(),
            'amount': forms.NumberInput(),
            'category': forms.Select(),
            'date': forms.SelectDateWidget()
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput()
        }


class RestrictedExpenseForm(AddExpenseForm):
    class Meta(AddExpenseForm.Meta):
        exclude = ['name', 'amount', 'date']
