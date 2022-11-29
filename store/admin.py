from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Product, Attribute, AttributeValue, Image, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # model = CustomUser
    list_display = (
        "name",
        "price",
    )
    # list_filter = ("name",)
    # fieldsets = ((None, {"fields": ("name", "price", "category")}),)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    # model = CustomUser
    list_display = ("name",)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    # model = CustomUser
    list_display = ("value", "attribute")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # model = Image
    list_display = ("title", "url")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # model = CustomUser
    list_display = ("name",)
