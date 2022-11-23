from django.urls import path
from .views import index, MyLoginView, UserSignupView, AddressView

urlpatterns = [
    path("", index, name="index"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("address/", AddressView.as_view(), name="address"),
]
