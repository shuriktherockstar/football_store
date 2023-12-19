from django.contrib import admin

from football_store.utlis import register_all_models
from products.models import ProductUnit, ProductUnitProperty


class ProductUnitPropertyInline(admin.TabularInline):
    model = ProductUnitProperty
    extra = 1


class ProductUnitAdmin(admin.ModelAdmin):
    inlines = [ProductUnitPropertyInline]


admin.site.register(ProductUnit, ProductUnitAdmin)

register_all_models('admin')
