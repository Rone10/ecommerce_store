from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, TemplateView
from django.views import View
from .models import Product
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.


class ProductDetailView(DetailView):
    template_name = "store/product_detail.html"
    model = Product
    context_object_name = "product"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     prod = Product.objects.get(name="Air Jordan")
    #     context["product"] = prod
    #     # context["image"] = prod.product_image[0]
    #     return context


class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset
        queryset = super().get_queryset()
        # Get the q GET parameter
        q = self.request.GET.getlist(
            "color[]"
        )  # lookup how to return multiple input values
        print(q)
        if q:
            # Return a filtered queryset
            sess = self.request.session
            print(f"sess: {sess}")
            res = queryset.filter(category__name__in=q)
            print(f"res: {res}")
            return res
        # Return the base queryset
        return queryset


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product = Product.objects.get(pk=product_id)
        recently_viewed_products = None

        if "recently_added" in request.session:
            # if product_id in request.session["recently_added"]:
            #     request.session["recently_viewed"].remove(product_id) # later for removing item from cart

            # products = Product.objects.filter(pk__in=request.session["recently_added"])
            # recently_viewed_products = sorted(
            #     products, key=lambda x: request.session["recently_added"].index(x.id)
            # )
            request.session["recently_added"].insert(0, product_id)
            # if len(request.session["recently_viewed"]) > 5:
            #     request.session["recently_viewed"].pop()
        else:
            request.session["recently_added"] = [product_id]
            # return HttpResponseRedirect(reverse_lazy("products:cart"))

        request.session.modified = True

        # context = {
        #     "product": product,
        #     "recently_viewed_products": recently_viewed_products,
        # }
        # return render(request, "store/cart.html", context)
        return HttpResponseRedirect(reverse_lazy("products:cart_view"))


class CartView(TemplateView):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = None
        recently_added_products = None
        if "recently_added" in self.request.session:
            products = Product.objects.filter(
                pk__in=self.request.session["recently_added"]
            )
        else:
            self.request.session["recently_added"] = []
            return context
        if products:
            recently_added_products = sorted(
                products,
                key=lambda x: self.request.session["recently_added"].index(x.id),
            )
        # request.session["recently_viewed"].insert(0, product_id)
        context["products"] = recently_added_products
        return context


"""
on product detail page, click add to cart and take product id and push it 
onto a cart list in a session variable.

When cart is clicked, grab the session varaible containing the cart items and 
iterate over them and render them on the page by looking them up in the db.

When user clicks checkout, grab cart items from session variable and create an order 
item from the Orders model.


"""
# class ProductSearchListView(ListView):
#     model = Product
