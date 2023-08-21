from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import pytest
from factories import UserFactory, AddressFactory
from accounts.models import Address, CustomUserManager

pytestmark = pytest.mark.django_db


class TestUser:
    def test_create_user(self, user_factory):
        user = user_factory(
            username="rone",
            email="rone@email.com",
        )
        assert user.username == "rone"
        assert user.email == "rone@email.com"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert str(user) == "rone@email.com"
        assert user.phone == "1234"
        assert get_user_model().objects.count() == 1

    def test_create_superuser(self, user_factory):
        user = user_factory(
            username="rone",
            email="rone@email.com",
            is_superuser=True,
            is_staff=True,
        )
        assert user.username == "rone"
        assert user.email == "rone@email.com"
        assert user.is_active
        assert user.is_staff
        assert user.is_superuser

    def test_create_user_missing_email(self, user_factory):
        with pytest.raises(IntegrityError) as e:
            user_factory(
                username="rone",
                email=None,
            )  # noqa
            print("e===", e)
        assert "NOT NULL constraint failed:" in str(e.value)

    def test_unique_email(self, user_factory):
        with pytest.raises(IntegrityError) as e:
            user_factory(
                email="one@email.com",
            )
            user_factory(
                email="one@email.com",
            )
        assert "UNIQUE constraint failed:" in str(e.value)

    @pytest.mark.xfail(reason="Phone Max Length")
    def test_check_phone_max_length(self, user_factory):
        with pytest.raises(Exception):
            user_factory(
                phone="12345678901234567890123456789012345678901234567890123456789012345678901234567890"
            )

    def test_custom_user_manager(self, user_factory):
        user = get_user_model().objects.create_user(
            username="rone",
            email="rone@email.com",
            password="yababulotest",
        )
        assert user.username == "rone"

    def test_custom_user_manager_create_user_missing_email(self, user_factory):
        with pytest.raises(ValueError) as e:
            get_user_model().objects.create_user(
                username="rone",
                email="",
                password="yababulotest",
            )

    def test_custom_user_manager_create_superuser(self, user_factory):
        user = get_user_model().objects.create_superuser(
            email="rone@email.com",
            password="yababulotest",
        )
        assert user.email == "rone@email.com"

    def test_custom_user_manager_create_superuser_is_staff_is_false(self, user_factory):
        with pytest.raises(ValueError) as e:
            user = get_user_model().objects.create_superuser(
                email="rone@email.com",
                password="yababulotest",
                is_staff=False,
            )

    def test_custom_user_manager_create_superuser_is_super_user_is_false(
        self, user_factory
    ):
        with pytest.raises(ValueError) as e:
            user = get_user_model().objects.create_superuser(
                email="rone@email.com",
                password="yababulotest",
                is_superuser=False,
            )


class TestAddress:
    def test_create_address(self, address_factory):
        address = address_factory(street="100 Street", country="Canada")
        assert address.street == "100 Street"
        assert address.city == "test city"
        assert address.state == "test state"
        assert address.postal_code == "12345"
        assert address.country == "Canada"
        assert str(address) == "100 Street"
        assert address.user.email == "test@email.com"

    def test_address_country_default(self, address_factory):
        address = address_factory()
        assert address.country == "United States"
