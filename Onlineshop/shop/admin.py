from django.contrib import admin
from .models import Category, Product, ProductFeature, ProductImage
# Register your models here.


# --- Inlines ---

class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class FeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created', 'updated', 'off', 'offer_price')
    list_filter = ('available', 'created', 'updated', 'category')
    list_editable = ('price', 'stock', 'available', 'off', 'offer_price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline, FeatureInline]
    
    
# @admin.register(ProductFeature)
# class ProductFeatureAdmin(admin.ModelAdmin):
#     list_display = ('product', 'feature_name', 'feature_value')
#     search_fields = ('feature_name', 'feature_value', 'product__name')
    
    
# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image')
#     search_fields = ('product__name',)
