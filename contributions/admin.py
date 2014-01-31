from django.contrib import admin

from models import ProductContribution, Sponsorship, Project

class ProductContributionAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'persona_id', 'role')
    list_filter = ('role',)
    search_fields = ['product_id__title', 'product_id__ean', 'persona_id__name_surname']
    
admin.site.register(ProductContribution, ProductContributionAdmin)
admin.site.register(Sponsorship)
admin.site.register(Project)
