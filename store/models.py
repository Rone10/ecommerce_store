from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ManyToManyField("store.Category", related_name="categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        "store.Attribute", related_name="attribute_value", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.value


class Order(models.Model):
    pass


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
