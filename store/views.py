from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, TemplateView
from django.views import View
from .models import Product, Order, OrderItem
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


class ProductDetailView(DetailView):
    template_name = "store/product_detail.html"
    model = Product
    context_object_name = "product"

    # def get_queryset(self):
    #     super().get_queryset()
    #     product = Product.objects.filter(pk=self.kwargs["pk"])
    #     return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs["pk"]
        print(f"product_id: {self.object.id}")
        product = Product.objects.get(pk=product_id)
        recently_viewed_products = None
        print(f"pr {self.object}")

        if "recently_viewed" in self.request.session:
            if product_id in self.request.session["recently_viewed"]:
                self.request.session["recently_viewed"].remove(
                    product_id
                )  # later for removing item from cart

            products = Product.objects.filter(
                pk__in=self.request.session["recently_viewed"]
            )
            recently_viewed_products = sorted(
                products,
                key=lambda x: self.request.session["recently_viewed"].index(x.id),
            )
            self.request.session["recently_viewed"].insert(0, product_id)
            if len(self.request.session["recently_viewed"]) > 4:
                self.request.session["recently_viewed"].pop()
        else:
            self.request.session["recently_viewed"] = [product_id]
        self.request.session.modified = True
        context["recently_viewed_products"] = recently_viewed_products
        return context


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
    """
    if user is not logged in, item will be added to cart session using product_id.
    Once user logs in, items in session cart will be transferred to logged in user cart and
    session cart emptied.

    session cart should persist even after browser closure.

    """

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(pk=product_id)
        recently_viewed_products = None

        if self.request.user.is_authenticated:
            print("inside if user authenticated")
            # old_item = OrderItem.objects.get(
            #     customer=self.request.user, product=product
            # ) # this raises a DoesNotExit error if the object is not found and that causes
            old_item = OrderItem.objects.filter(
                customer=self.request.user, product=product, is_placed=False
            ).first()
            print("***** .before if old_items:")
            if old_item:
                old_item.quantity += 1
                old_item.save()
            else:
                print("_-_-_ inside else: for new_items:")
                new_item = OrderItem.objects.create(
                    customer=self.request.user, product=product
                )
                new_item.save()

        elif "recently_added" in self.request.session:
            # if product_id in request.session["recently_added"]:
            #     request.session["recently_viewed"].remove(product_id) # later for removing item from cart

            # products = Product.objects.filter(pk__in=request.session["recently_added"])
            # recently_viewed_products = sorted(
            #     products, key=lambda x: request.session["recently_added"].index(x.id)
            # )
            self.request.session["recently_added"].insert(0, product_id)
            # if len(request.session["recently_viewed"]) > 5:
            #     request.session["recently_viewed"].pop()
        else:
            self.request.session["recently_added"] = [product_id]
            # return HttpResponseRedirect(reverse_lazy("products:cart"))

        self.request.session.modified = True

        # context = {
        #     "product": product,
        #     "recently_viewed_products": recently_viewed_products,
        # }
        # return render(request, "store/cart.html", context)
        message = "successfully added to cart"
        messages.info(self.request, message)
        return HttpResponseRedirect(reverse_lazy("products:cart_view"))


class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(pk=product_id)
        recently_viewed_products = None

        if self.request.user.is_authenticated:
            item = OrderItem.objects.filter(
                customer=self.request.user, product=product
            ).first()
            if item:
                item.delete()
        elif "recently_added" in self.request.session:
            self.request.session["recently_added"].remove(product_id)
            self.request.session.modified = True
        else:
            return HttpResponseRedirect(reverse_lazy("products:list"))
        return HttpResponseRedirect(reverse_lazy("products:cart_view"))


class CartView(TemplateView):
    """
    if user is logged in, show user cart otherwise grab session cart
    """

    template_name = "store/cart.html"
    # def get(self, request, *args, **kwargs):
    #     # product_id = self.kwargs["pk"]
    #     # product = Product.objects.get(pk=product_id)
    #     # recently_viewed_products = None
    #     print(f"request.sessions: {self.request.session['recently_added']}:")
    #     if self.request.user.is_authenticated:
    #         print("CartView.get()")
    # old_item = OrderItem.objects.filter(
    #     customer=self.request.user, product=product
    # ).first()
    # if old_item:
    #     old_item.quantity += 1
    #     old_item.save()
    # else:
    #     new_item = OrderItem.objects.create(
    #         customer=self.request.user, product=product
    #     )
    #     new_item.save()

    #     for id in self.request.session["recently_added"]:
    #         print("CartView.get().if")
    #         prod = Product.objects.get(pk=id)
    #         if OrderItem.objects.filter(
    #             customer=self.request.user, product=prod
    #         ).first():
    #             self.request.session["recently_added"].remove(id)
    #         else:
    #             OrderItem.objects.create(customer=self.request.user, product=prod)
    #         request.session.modified = True
    # # elif "recently_added" in self.request.session:

    # #     self.request.session["recently_added"].insert(0, product_id)
    # # else:
    # # self.request.session["recently_added"] = [product_id]
    # print("outside for loop")
    # return render(self.request, "store/cart.html")

    # request.session.modified = True
    # return HttpResponseRedirect(reverse_lazy("products:cart_view"))

    def get_context_data(self, **kwargs):
        print("inside get_context_data")
        context = super().get_context_data(**kwargs)
        products = None
        recently_added_products = None
        if self.request.user.is_authenticated:
            context["user_cart"] = OrderItem.objects.filter(
                customer=self.request.user, is_placed=False
            )
            if "recently_added" in self.request.session:
                print(f" self.request.session {self.request.session['recently_added']}")
                if self.request.session["recently_added"]:
                    for id in self.request.session["recently_added"]:
                        print("for id in self.request.session['recently_added']:")
                        prod = Product.objects.get(pk=id)
                        if OrderItem.objects.filter(
                            customer=self.request.user, product=prod
                        ).first():
                            self.request.session["recently_added"].remove(id)
                        else:
                            OrderItem.objects.create(
                                customer=self.request.user, product=prod
                            )
                        print('about to delete "recently_added"')
                print(
                    f"before del request.session {self.request.session['recently_added']}"
                )
                del self.request.session["recently_added"]
                # print(
                #     f"after del request.session {[sess for sess in self.request.session]}"
                # )
                self.request.session.modified = True
        if "recently_added" in self.request.session:
            print("if recently_added:  ")
            products = Product.objects.filter(
                pk__in=self.request.session["recently_added"]
            )
        else:
            print('adding self.request.session["recently_added"]')
            self.request.session["recently_added"] = []
            # return context
        if products:
            recently_added_products = sorted(
                products,
                key=lambda x: self.request.session["recently_added"].index(x.id),
            )
        # request.session["recently_viewed"].insert(0, product_id)

        context["products"] = recently_added_products
        return context


# def CheckoutView(request):

#     return HttpResponseRedirect(reverse_lazy("products:list"))


class OrdersListView(ListView):
    template_name = "store/order_summary.html"
    context_object_name = "orders"

    def get_queryset(self):
        # queryset = super().get_queryset()
        return Order.objects.filter(customer=self.request.user).all()


class CheckoutView(ListView):
    """
    once user clicks checkout:
        1. log user in and redirect them to cart page
        2. access the recently_viewed session:
        3. iterate over its items and add them to your order model to create an order
    """

    template_name = "store/order_summary.html"
    context_object_name = "orders"

    def get(self, request, *args, **kwargs):
        order = Order.objects.create(customer=self.request.user)
        items = OrderItem.objects.filter(
            customer=self.request.user, is_placed=False
        ).all()
        if items:
            for item in items:
                order.order_items.add(item)
                item.is_placed = True
                item.save()

        order.save()
        # return render(request, "store/order_summary.html")
        # return super().get(request, *args, **kwargs)
        message = "successfully placed order"
        messages.info(self.request, message)
        return HttpResponseRedirect(
            reverse_lazy("products:order_detail", kwargs={"pk": order.id})
        )

    def get_queryset(self):
        # queryset = super().get_queryset()
        return Order.objects.filter(customer=self.request.user).all()


class OrderDetailView(View):

    # context_object_name = "order"

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs["pk"], customer=self.request.user)
        context = {"order": order}
        return render(request, "store/checkout_confirm.html", context)


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
