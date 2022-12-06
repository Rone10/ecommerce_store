from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("detail/<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("list/", views.ProductListView.as_view(), name="list"),
    path("<int:pk>/add-to-cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart-items/", views.CartView.as_view(), name="cart_view"),
    path("checkout/", login_required(views.CheckoutView), name="checkout"),
    # path("address/", AddressView.as_view(), name="address"),
]
