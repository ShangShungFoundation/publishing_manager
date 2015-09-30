from django.contrib import admin

from products.models import ESUPPORT_TYPES
from catalogs.models import Item

from models import Client
from models import EProduct, Delivery


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname',  'password', 'email')
    search_fields = ('surname', 'email')
    raw_id_fields=('customer',) 
    #readonly_fields = ("created_by", )

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'surname'),
                "password",
                'email',
                'customer',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


class EProductAdmin(admin.ModelAdmin):
    list_display = ('item',)
    search_fields = ('item__product__title', 'item__product__ean')
    #raw_id_fields=('item',) 
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['item'].queryset = Item.objects.filter(
             catalog_id=3, product__support_type__in=ESUPPORT_TYPES)
         return super(EProductAdmin, self).render_change_form(request, context, args, kwargs)


class DeliveryAdmin(admin.ModelAdmin):
    #list_display = ('client',)
    search_fields = ('client__email', )
    raw_id_fields=('eproduct', 'client') 
    readonly_fields = ("created_by", "created_at" )

    fieldsets = (
        (None, {
            'fields': (
                       ( 'client', 'eproduct'),
                       ( 'created_by', 'created_at'),
                       'order',
                       )
        }),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(Client, ClientAdmin)
admin.site.register(EProduct, EProductAdmin)
admin.site.register(Delivery, DeliveryAdmin)
