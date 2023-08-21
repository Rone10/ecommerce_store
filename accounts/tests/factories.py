import factory
from django.contrib.auth import get_user_model
from accounts.models import Address

# from accounts.forms import UserCreateForm, CustomLoginForm, AddressForm


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    # username = "test"
    first_name = ("mawdo",)
    last_name = "rone"
    email = "test@email.com"
    phone = "1234"
    password = "test"
    is_superuser = False
    is_staff = False
    is_active = True


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(UserFactory)
    street = "1234 test street"
    city = "test city"
    state = "test state"
    postal_code = "12345"
    # country = "United States"


# class UserCreateFormFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         form = UserCreateForm

#     first_name = "test"
#     last_name = "test"
#     email = "test@email.com"
#     password1 = "test"
#     password2 = "test"


# class CustomLoginFormFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = CustomLoginForm

#     username = "test"
#     password = "test"


# class AddressFormFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = AddressForm

#     street = "1234 test street"
#     city = "test city"
#     postal_code = "12345"
#     country = "United States"
