from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# class UserProfileForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'country', 'phone', 'avatar')


class RegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма профиля пользователя"""

    class Meta:
        model = User
        fields = ('username', 'country', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        """Скрытие поля password"""
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class ListUserForm(StyleFormMixin, forms.ModelForm):
    """Форма модели User для списка"""
    pass
    # class Meta:
    #     model = User
    #     fields = ('email', 'phone', 'country', )


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=4)
