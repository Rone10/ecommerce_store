from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("detail/<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("list/", views.ProductListView.as_view(), name="list"),
    path("<int:pk>/add-to-cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart-items/", views.CartView.as_view(), name="cart_view"),
    path("checkout/", login_required(views.CheckoutView.as_view()), name="checkout"),
    path(
        "remove-from-cart/<int:pk>/",
        views.RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "order-detail/<int:pk>",
        views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "orders/",
        views.OrdersListView.as_view(),
        name="orders",
    ),
]
