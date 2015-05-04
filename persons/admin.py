from django.contrib import admin

from models import Persona, Author

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('name_surname', 'country', 'email')
    search_fields = ['name_surname', 'email']
    
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Author)

