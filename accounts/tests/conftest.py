from pytest_factoryboy import register

from factories import (
    UserFactory,
    AddressFactory,
)

register(UserFactory)
register(AddressFactory)
