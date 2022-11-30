from django.urls import path
from . import views

urlpatterns = [
    path("detail/<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("list/", views.ProductListView.as_view(), name="list"),
    path("<int:product_id>/cart/", views.AddToCartView.as_view(), name="cart"),
    path("cart-items/", views.CartView.as_view(), name="cart_view"),
    # path("signup/", UserSignupView.as_view(), name="signup"),
    # path("address/", AddressView.as_view(), name="address"),
]
