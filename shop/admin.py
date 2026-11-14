from django.contrib import admin
from .models import Category, Product, Order, OrderItem

admin.site.site_header = "Aýakgap dükany - Admin"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "price", "in_stock", "featured")
    list_filter = ("category", "in_stock", "featured")
    search_fields = ("name", "brand")
    prepopulated_fields = {"slug": ("name",)}

class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "total", "created")
    inlines = [ItemInline]
