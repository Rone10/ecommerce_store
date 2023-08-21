import factory
from django.contrib.auth import get_user_model
from store.models import (
    Product,
    Category,
    Order,
    OrderItem,
    Image,
    Attribute,
    AttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "test category"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = "rone"
    last_name = "wazza"
    email = "rone@email.com"
    phone = "1234"
    password = "mytestpassword"
    is_superuser = False
    is_staff = False
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test product"
    description = "test description"
    price = 10
    # category = factory.SubFactory(CategoryFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    # customer = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    created_at = "2021-01-01 00:00:00"


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory)
    created_at = "2021-01-01 00:00:00"
    # order_items = factory.SubFactory(OrderItemFactory)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    product = factory.SubFactory(ProductFactory)
    url = "test_image.jpg"
    alt_text = "test alt"
    title = "test image title"


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "test attribute"
    product = factory.SubFactory(ProductFactory)


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute = factory.SubFactory(AttributeFactory)
    value = "test value"
