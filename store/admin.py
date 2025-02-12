from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from . import models



class CustomInventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'LOW')
        ]
        
    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
    


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', CustomInventoryFilter]
    ordering = ['inventory']
    list_per_page = 20
    list_select_related = ['collection']
    
    def collection_title(self, product):
        return product.collection.title
    
    def inventory_status(self, product):
        if product.inventory < 10:
            return "LOW"
        return "OK"
    


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10
    
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = reverse("admin:store_order_changelist") + "?" + urlencode({'customer__id':str(customer.id)})
        return format_html(f'<a href="{url}">{customer.orders_count}</a>')
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))




@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer_name']
    list_editable = ['payment_status']
    list_select_related = ['customer']
    
    
    def customer_name(self, order):
        return order.customer.full_name()


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse("admin:store_product_changelist") + "?" + urlencode({"collection__id": str(collection.id)})
        return format_html(f'<a href="{url}">{collection.products_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))