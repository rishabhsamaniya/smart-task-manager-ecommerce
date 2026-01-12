from django.contrib import admin
from .models import (
    Category, Tag, Product,ProductImage,
    Cart, CartItem, Order, OrderItem
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock_quentity", "is_active")
    list_filter = ("is_active", "category", "tags")

    inlines = [ProductImageInline]

    fieldsets = (
        ("Basic Info",{
            "fields": ("name", "category", "tags", "is_active")
        }),

        ("Descriptions",{
            "fields": ("short_description", "description", "specifications")
        }),

        ("Pricing & Stock", {
            "fields": ("price", "stock_quentity")
        })

    )



# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Product)
# admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)