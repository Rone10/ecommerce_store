from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Product

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
