from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import pytest

from store.tests.factories import (
    ProductFactory,
    UserFactory,
    OrderFactory,
    OrderItemFactory,
    CategoryFactory,
    ImageFactory,
    AttributeFactory,
    AttributeValueFactory,
)
from store.models import (
    Product,
    Order,
    Category,
    OrderItem,
    Image,
    Attribute,
    AttributeValue,
)


pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_category_model(self, category_factory):
        category = category_factory()
        assert category.name == "test category"

    def test_category_model_repr(self, category_factory):
        category = category_factory()
        assert repr(category) == "Category: test category"

    def test_str_method(self, category_factory):
        category = category_factory()
        assert str(category) == "test category"


class TestProductModel:
    def test_product_model(self, product_factory, category_factory):
        product = product_factory()
        category = category_factory()
        product.category.add(category)
        product.save()
        assert Product.objects.count() == 1
        assert product.name == "test product"
        assert product.description == "test description"
        assert product.price == 10
        assert product.category.all()[0].name == "test category"

    def test_product_model_repr(self, product_factory, category_factory):
        product = product_factory()
        category = category_factory()
        product.category.add(category)
        product.save()
        assert repr(product) == "Product: test product"

    def test_product_model_get_absolute_url(self, product_factory, category_factory):
        product = product_factory()
        category = category_factory()
        product.category.add(category)
        product.save()
        assert product.get_absolute_url() == f"/products/detail/{product.pk}/"

    def test_str_method(self, product_factory, category_factory):
        product = product_factory()
        category = category_factory()
        product.category.add(category)
        product.save()
        assert str(product) == "test product"


class TestImageModel:
    def test_image_model(self, image_factory, product_factory, category_factory):
        image = image_factory()
        category = category_factory()
        image.product.category.add(category)
        image.save()
        assert Image.objects.count() == 1
        assert image.url == "test_image.jpg"
        assert image.product.name == "test product"
        assert image.title == "test image title"

    def test_str_method(self, image_factory, product_factory):
        image = image_factory()
        image.save()
        assert str(image) == "test image title"


class TestOrderItemModel:
    def test_order_item_model(self, user_factory, order_item_factory, product_factory):
        customer = user_factory()
        product = product_factory()

        order_item = OrderItem.objects.create(
            customer=customer,
            product=product,
            quantity=1,
            created_at="2021-01-01 00:00:00",
        )

        assert OrderItem.objects.count() == 1
        assert order_item.quantity == 1
        assert order_item.product.name == "test product"

    def test_str_method(self, user_factory, order_item_factory, product_factory):
        customer = user_factory()
        product = product_factory()

        order_item = OrderItem.objects.create(
            customer=customer,
            product=product,
            quantity=1,
            created_at="2021-01-01 00:00:00",
        )
        assert str(order_item) == "test product"

    def test_order_item_total(self, user_factory, order_item_factory, product_factory):
        customer = user_factory()
        product = product_factory()

        order_item = OrderItem.objects.create(
            customer=customer,
            product=product,
            quantity=1,
            created_at="2021-01-01 00:00:00",
        )
        assert order_item.total() == 10


class TestOrderModel:
    def test_order_model(
        self, user_factory, order_factory, order_item_factory, product_factory
    ):
        customer = user_factory()
        product = product_factory()

        order_item = OrderItem.objects.create(
            customer=customer,
            product=product,
            quantity=1,
            created_at="2021-01-01 00:00:00",
        )
        order = Order.objects.create(
            customer=customer,
            created_at="2021-01-01 00:00:00",
        )
        order.order_items.add(order_item)
        order.save()

        assert Order.objects.count() == 1
        assert order.order_items.all()[0].product.name == "test product"
        assert order.order_items.all()[0].quantity == 1
        assert order.order_items.all()[0].total() == 10
        assert order.get_order_total() == 10


class TestAttributeModel:
    def test_attribute_model(self, attribute_factory):
        attribute = attribute_factory()
        assert Attribute.objects.count() == 1
        assert attribute.name == "test attribute"
        assert attribute.product.name == "test product"
        assert attribute.product.price == 10

    def test_attribute_model_repr(self, attribute_factory):
        attribute = attribute_factory()
        assert repr(attribute) == "Attribute: test attribute"

    def test_str_method(self, attribute_factory):
        attribute = attribute_factory()
        assert str(attribute) == "test attribute"


class TestAttributeValueModel:
    def test_attribute_value_model(self, attribute_value_factory):
        attribute_value = attribute_value_factory()
        assert AttributeValue.objects.count() == 1
        assert attribute_value.value == "test value"
        assert attribute_value.attribute.name == "test attribute"
        assert attribute_value.attribute.product.name == "test product"
        assert attribute_value.attribute.product.price == 10

    def test_attribute_value_model_repr(self, attribute_value_factory):
        attribute_value = attribute_value_factory()
        assert repr(attribute_value) == "AttributeValue: test value"

    def test_str_method(self, attribute_value_factory):
        attribute_value = attribute_value_factory()
        assert str(attribute_value) == "test value"
