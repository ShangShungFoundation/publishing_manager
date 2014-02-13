from django.contrib import admin

from models import Catalog, Item

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name',  'web', 'publisher', 'is_active')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('product',  'catalog', 'url', 'price')
    list_filter = ( 'catalog', 'product__support_type', 'product__on_sale', 'product__restriction',) 
    search_fields = ['product__title', 'product__ean',  'product__code', ]
    
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Item, ItemAdmin)