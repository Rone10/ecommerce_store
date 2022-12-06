from django.db import models
from django.urls import reverse
from django.conf import settings

# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(in_stock=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ManyToManyField("store.Category", related_name="categories")
    # in_stock = models.BooleanField(default=True)
    # stock = models.IntegerField()

    # objects = models.Manager()
    # products = ProductManager()
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"


class Image(models.Model):
    product = models.ForeignKey(
        "store.Product", related_name="product_image", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    url = models.ImageField(upload_to="products")
    alt_text = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(
        "store.Product", related_name="attribute_name", on_delete=models.CASCADE
    )

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        "store.Attribute", related_name="attribute_value", on_delete=models.CASCADE
    )

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.value}"

    def __str__(self):
        return self.value


class OrderItem(models.Model):
    """ """

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # for identifying cart owner
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_placed = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    def total(self):
        return self.quantity * self.product.price


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_items = models.ManyToManyField("store.OrderItem")

    def get_order_total(self):
        total = 0
        for item in self.order_items.all():
            total += item.total()
        return total


# Create your models here.
"""
Preliminary Field List

product name
product category
product expiry date
product description
product images
product price
product quantity
product rating
product colors

customer first name
customer last name
customer address
customer email
customer phone number 

order date placed
order total ($)
order item (product)
order number 
order delivery date
order delivery status 



"""
