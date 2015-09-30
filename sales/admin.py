from django.contrib import admin

# Register your models here.
from models import Order, OrderItem

class ItemInline(admin.StackedInline):
    model = OrderItem
    max_num = 1
    
class OrderAdmin(admin.ModelAdmin):
    #date_hierarchy = 'created'
    list_display = ("created", 'created_by','total', 'paid')
    list_filter = ( 'created_by', )
    inlines = [ItemInline]
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)