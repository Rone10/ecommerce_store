import pytest

from django.urls import reverse
from django.test.utils import override_settings

# from django.contrib.auth.models import User
# from django.test import Client
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from accounts.models import Address
from accounts.forms import CustomLoginForm, UserCreateForm, AddressForm
from accounts.views import MyLoginView, UserSignupView, AddressView
from accounts.tests.factories import UserFactory, AddressFactory


from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects
from pytest_django.asserts import assertContains
from pytest_django.asserts import assertNotContains
from pytest_django.asserts import assertFormError
from pytest_django.asserts import assertTemplateNotUsed
from pytest_django.asserts import assertJSONEqual
from pytest_django.asserts import assertQuerysetEqual
from pytest_django.asserts import assertNumQueries


pytestmark = pytest.mark.django_db


class TestIndexView:
    def test_index_view(self, client):
        response = client.get(reverse("accounts:home"))
        assert response.status_code == 200


class TestLoginView:
    def test_login_view_get(self, client):
        response = client.get(reverse("accounts:login"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/login.html")

    def test_login_view_post(self, client, user_factory):
        user = get_user_model().objects.create_user(
            first_name="mawdo",
            last_name="rone",
            email="mawdorone@email.com",
            password="password_test",
        )

        assert get_user_model().objects.count() == 1
        response = client.post(
            reverse("accounts:login"),
            data={
                "username": user.email,
                "password": "password_test",
            },
        )
        assertRedirects(response, reverse("accounts:home"), status_code=302)
        response = client.login(email=user.email, password="Ghassan123")


class TestSignupView:
    def test_signup_view_get(self, client):
        response = client.get(reverse("accounts:signup"))
        assert response.status_code == 200

    def test_signup_view_post(self, client, user_factory):
        response = client.post(
            reverse("accounts:signup"),
            {
                "username": "test",
                "first_name": "mawdo",
                "last_name": "rone",
                "email": "test@email.com",
                "password1": "password_test",
                "password2": "password_test",
            },
        )
        assert get_user_model().objects.count() == 1
        assert response.status_code == 302

    def test_signup_view_success_redirect(self, client):
        response = client.post(
            "/accounts/signup/",
            data={
                "email": "tissalbaba@email.com",
                "password1": "testpass123",
                "password2": "testpass123",
                "first_name": "Ghassan",
                "last_name": "Tissali",
            },
        )

        assertRedirects(response, reverse("accounts:login"), status_code=302)
        user = get_user_model().objects.get(email="tissalbaba@email.com")
        assert user is not None
        assert get_user_model().objects.count() == 1


class TestAddressView:
    def test_address_view_get(self, client, user_factory):
        user = get_user_model().objects.create_user(
            first_name="mawdo",
            last_name="rone",
            email="mawdorone@gmail.com",
            password="password_test",
        )
        data = {
            "street": "1234 test street",
            "city": "test city",
            "postal_code": "12345",
            "country": "United States",
        }
        client.login(username=user.email, password="password_test")
        response = client.post(
            reverse("accounts:address"),
            data=data,
        )
        assert response.status_code == 302
