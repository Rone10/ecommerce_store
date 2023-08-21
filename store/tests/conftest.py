from pytest_factoryboy import register
import pytest

from store.tests.factories import (
    ProductFactory,
    CategoryFactory,
    OrderFactory,
    OrderItemFactory,
    UserFactory,
    ImageFactory,
    AttributeFactory,
    AttributeValueFactory,
)

register(ProductFactory)
register(CategoryFactory)
register(OrderFactory)
register(OrderItemFactory)
register(UserFactory)
register(ImageFactory)
register(AttributeFactory)
register(AttributeValueFactory)
