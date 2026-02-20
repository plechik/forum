from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Iм'я користувача",
    )
    email = forms.EmailField(
        required=True,
        label='Email'
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Підтвердження пароля"

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = ""
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'