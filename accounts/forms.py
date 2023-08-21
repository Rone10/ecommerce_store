from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms.widgets import PasswordInput, EmailInput, TextInput
from .models import CustomUser, Address


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=EmailInput(
            attrs={"class": "email", "placeholder": "Email", "id": "email"}
        )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                "class": "email",
                "placeholder": "Enter P",
                "id": "passwordsss",
            }
        )
    )


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        widget=TextInput(
            attrs={"class": "email", "id": "first_name", "placeholder": "First Name"}
        )
    )
    last_name = forms.CharField(
        widget=TextInput(
            attrs={"class": "email", "id": "lasts_name", "placeholder": "Last Name"}
        )
    )
    email = forms.CharField(
        widget=EmailInput(
            attrs={"class": "email", "placeholder": "Email", "id": "email"}
        )
    )

    password1 = forms.CharField(
        widget=PasswordInput(
            attrs={"class": "email", "placeholder": "Password", "id": "password1"}
        )
    )

    password2 = forms.CharField(
        widget=PasswordInput(
            attrs={
                "class": "email",
                "placeholder": "Re-type Password",
                "id": "password2",
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class AddressForm(forms.ModelForm):
    street = forms.CharField(
        widget=TextInput(
            attrs={"class": "email", "id": "street", "placeholder": "Enter Street Name"}
        )
    )
    city = forms.CharField(
        widget=TextInput(
            attrs={"class": "email", "id": "city", "placeholder": "Enter City Name"}
        )
    )
    postal_code = forms.CharField(
        widget=TextInput(
            attrs={"class": "email", "id": "street", "placeholder": "Enter Postal Code"}
        )
    )
    country = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "email",
                "id": "country",
                "placeholder": "Enter Country Name",
            }
        )
    )

    class Meta:
        model = Address
        fields = ["street", "city", "postal_code", "country"]
