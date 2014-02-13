from django.contrib import admin

from models import Company, Distribution

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',  'email', 'country', 'activity', 'is_active')
    search_fields = ['name', 'email']
    
admin.site.register(Company, CompanyAdmin)
admin.site.register(Distribution)
