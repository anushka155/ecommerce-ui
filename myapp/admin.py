from django.contrib import admin
from .models import Product,Order


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    search_fields = ('name', 'short_description')
    readonly_fields = ('created_at', 'slug')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['uid', 'buyer_name', 'created_at'] 
    list_filter = ['created_at']
    readonly_fields = ['created_at']


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
