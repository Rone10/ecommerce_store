from django.urls import path
from . import views

urlpatterns = [
    path("detail/<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("list/", views.ProductListView.as_view(), name="list"),
    # path("signup/", UserSignupView.as_view(), name="signup"),
    # path("address/", AddressView.as_view(), name="address"),
]
