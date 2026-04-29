from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# This makes the Category model appear in the admin
admin.site.register(Category)

# This version of Product registration shows more info in the list view
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')
    list_filter = ('category',) # Adds a filter sidebar on the right
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)