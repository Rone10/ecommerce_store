from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm, UserCreateForm, AddressForm
from django.views.generic import CreateView
from .models import Address
from django.urls import reverse_lazy

# Create your views here.


def index(request):
    return render(request, "store/home.html")


class MyLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm
    success_url = reverse_lazy("accounts:index")


class UserSignupView(CreateView):
    form_class = UserCreateForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")


class AddressView(CreateView):
    form_class = AddressForm
    model = Address
    template_name = "registration/address.html"
    success_url = reverse_lazy("accounts:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
