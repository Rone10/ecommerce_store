from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import pytest
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist


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
from store.views import (
    ProductListView,
    ProductDetailView,
    AddToCartView,
    RemoveFromCartView,
    CartView,
    OrdersListView,
    OrderDetailView,
    CheckoutView,
)

pytestmark = pytest.mark.django_db


class TestProdcutListView:
    def test_product_list_view(self, client, product_factory):
        product = product_factory()
        response = client.get(reverse("products:list"))
        # response = ProductListView.as_view()(request)
        assert response.status_code == 200
        # print("\nresponse.rendered_content: ", response.rendered_content)
        assert product.name in response.rendered_content
        assert str(product.price) in response.rendered_content

    def test_product_list_view_search(self, client, product_factory, category_factory):
        category = category_factory(name="men")
        product = product_factory(
            name="test product", description="test description", price=10
        )
        product.category.add(category)
        product.save()
        response = client.get(reverse("products:list"), {"category": "men"})
        # print("\nresponse", response)
        assert response.status_code == 200
        assert product.name in response.rendered_content
        assert str(product.price) in response.rendered_content
        assert product.category.all()[0].name in response.rendered_content
        assert (
            product.category.all()[0].name
            == response.context["products"][0].category.all()[0].name
        )


class TestProductDetailView:
    def test_product_detail_view(self, client, product_factory):
        product = product_factory()
        response = client.get(reverse("products:detail", kwargs={"pk": product.pk}))
        # response = ProductDetailView.as_view()(request, pk=product.pk)
        assert response.status_code == 200
        assert product.name in response.rendered_content
        assert str(product.price) in response.rendered_content

    def test_product_detail_view_404(self, client, product_factory):
        product = product_factory()
        response = client.get(reverse("products:detail", kwargs={"pk": 999}))
        assert response.status_code == 404

    def test_product_detail_view_get_context_data(
        self, client, product_factory, image_factory
    ):
        product = product_factory()
        image = image_factory(product=product)
        session = client.session
        session["recently_viewed"] = [product.pk]
        session.save()
        response = client.get(reverse("products:detail", kwargs={"pk": product.pk}))
        assert response.status_code == 200
        assert product.name in response.rendered_content
        assert str(product.price) in response.rendered_content
        assert image.product.name in response.rendered_content

    def test_product_detail_view_get_context_data_session(
        self, client, product_factory, image_factory
    ):
        product_1 = product_factory()
        product_2 = product_factory()
        product_3 = product_factory()
        product_4 = product_factory()
        product_5 = product_factory()
        image = image_factory(product=product_1)
        session = client.session
        session["recently_viewed"] = [product_1.pk]
        session["recently_viewed"] = [product_2.pk]
        session["recently_viewed"] = [product_3.pk]
        session["recently_viewed"] = [product_4.pk]
        session["recently_viewed"] = [product_5.pk]
        session.save()
        response = client.get(reverse("products:detail", kwargs={"pk": product_1.pk}))
        assert len(session["recently_viewed"]) < 5
        assert response.status_code == 200
        assert product_1.name in response.rendered_content
        assert str(product_1.price) in response.rendered_content
        assert image.product.name in response.rendered_content


class TestAddToCartView:
    def test_add_to_cart_view(self, client, product_factory):
        product = product_factory()
        product_2 = product_factory()
        session = client.session
        session["recently_added"] = [product_2.pk]
        session.save()
        response = client.get(
            reverse("products:add_to_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:cart_view")

    def test_add_to_cart_view_without_recently_added_session_key(
        self, client, product_factory
    ):
        product = product_factory()
        response = client.get(
            reverse("products:add_to_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:cart_view")
        assert client.session["recently_added"] == [product.pk]

    def test_add_to_cart_view_404(self, client, product_factory):
        with pytest.raises(ObjectDoesNotExist):
            product = product_factory()
            response = client.get(reverse("products:add_to_cart", kwargs={"pk": 999}))
            assert response.status_code == 404

    def test_add_to_cart_view_logged_in_user(
        self, client, product_factory, user_factory
    ):
        user = user_factory()
        client.force_login(user)
        product = product_factory()
        response = client.get(
            reverse("products:add_to_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:cart_view")
        assert OrderItem.objects.filter(customer=user).exists()

    def test_add_to_cart_view_logged_in_user_quantity_increase(
        self, client, product_factory, user_factory
    ):
        user = user_factory()
        client.force_login(user)
        product = product_factory()
        response = client.get(
            reverse("products:add_to_cart", kwargs={"pk": product.pk})
        )
        response = client.get(
            reverse("products:add_to_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:cart_view")
        assert OrderItem.objects.filter(customer=user).exists()


class TestRemoveFromCartView:
    def test_remove_from_cart_view_is_empty(self, client, product_factory):
        product = product_factory()
        response = client.get(
            reverse("products:remove_from_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:list")

    def test_remove_from_cart_view_user_is_logged_in(
        self, client, user_factory, product_factory
    ):
        user = user_factory()
        client.force_login(user)
        product = product_factory()
        client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
        response = client.get(
            reverse("products:remove_from_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:cart_view")

    def test_remove_from_cart_view_recently_added(self, client, product_factory):
        product = product_factory()
        session = client.session
        session["recently_added"] = [product.pk]
        session.save()
        response = client.get(
            reverse("products:remove_from_cart", kwargs={"pk": product.pk})
        )
        assert response.status_code == 302
        assert response.url == reverse("products:cart_view")


class TestCartView:
    def test_cart_view_user_is_logged_in(self, client, user_factory, product_factory):
        user = user_factory()
        client.force_login(user)
        product = product_factory()
        client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
        response = client.get(reverse("products:cart_view"))
        assert response.status_code == 200
        assert product.name in response.rendered_content

    def test_cart_view_user_is_logged_in_quantity_increase(
        self, client, user_factory, product_factory
    ):
        user = user_factory()
        client.force_login(user)
        product = product_factory()
        client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
        client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
        response = client.get(reverse("products:cart_view"))
        assert response.status_code == 200
        assert product.name in response.rendered_content


class TestCheckoutView:
    def test_checkout_view_user_is_logged_in(self, client, user_factory):
        user = user_factory()
        client.force_login(user)
        response = client.get(reverse("products:checkout"))
        assert response.status_code == 302

    def test_checkout_view_user_is_not_logged_in(self, client):
        response = client.get(reverse("products:checkout"))
        assert response.status_code == 302
        assert str(reverse("accounts:login")) in response.url

    def test_checkout_view_with_orders(self, client, product_factory, user_factory):
        product = product_factory()
        client
        user = user_factory()
        client.force_login(user)
        client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
        response = client.get(reverse("products:checkout"))

        assert response.status_code == 302
        assert (
            str(reverse("products:order_detail", kwargs={"pk": product.pk}))
            in response.url
        )


class TestOrderDetailView:
    def test_order_detail_view_user_is_logged_in(
        self, client, user_factory, product_factory
    ):
        user = user_factory()
        client.force_login(user)
        product = product_factory()
        client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
        client.get(reverse("products:checkout"))
        response = client.get(
            reverse("products:order_detail", kwargs={"pk": product.pk})
        )
        assert response.status_code == 200
        assert (
            product.name == response.context["order"].order_items.first().product.name
        )


# class TestOrderListView:
#     def test_order_list_view_user_is_logged_in(
#         self, client, user_factory, product_factory, request_factory
#     ):
#         user = user_factory()
#         client.force_login(user)
#         product = product_factory()
#         client.get(reverse("products:add_to_cart", kwargs={"pk": product.pk}))
#         client.get(reverse("products:checkout"))
#         response = client.get(reverse("products:orders"))
#         assert response.status_code == 200
#         assert (
#             product.name
#             == response.context["orders"].first().order_items.first().product.name
#         )
#         view = OrdersListView()
#         view.setup(request=request_factory())
#         queryset = view.get_queryset()

#         assert queryset.first().customer == user
