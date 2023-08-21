import pytest
from accounts.forms import UserCreateForm, AddressForm, CustomLoginForm

pytestmark = pytest.mark.django_db

user_create_form_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "test@email.com",
    "password1": "debunked",
    "password2": "debunked",
}
user_address_form_data = {
    "street": "1234 test street",
    "city": "test city",
    "postal_code": "12345",
    "country": "United States",
}


class TestUserCreateForm:
    def test_valid_form(self):
        form = UserCreateForm(data=user_create_form_data)
        assert form.is_valid()


class TestAddressForm:
    def test_valid_form(self):
        form = AddressForm(data=user_address_form_data)
        assert form.is_valid()


class TestCustomLoginForm:
    def test_valid_form(self):
        user = UserCreateForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@email.com",
                "password1": "debunked",
                "password2": "debunked",
            }
        )
        user.save()
        form = CustomLoginForm(
            data={"username": "johndoe@email.com", "password": "debunked"}
        )
        assert form.is_valid()
