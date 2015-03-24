from django.contrib import admin
from django.conf import settings

from models import Language, Masterpiece, Product, Edition, Book, CD, DVD, eBook, Game, Poster, AudioDownload, VideoDownload, Subject

from contributions.models import ProductContribution
from catalogs.models import Item

class BookInline(admin.StackedInline):
    model = Book
    max_num = 1


class eBookInline(admin.StackedInline):
    model = eBook
    max_num = 1


class CDInline(admin.StackedInline):
    model = CD
    max_num = 1


class DVDInline(admin.StackedInline):
    model = DVD
    max_num = 1


class GameInline(admin.StackedInline):
    model = Game
    max_num = 1


class AudioDownloadInline(admin.StackedInline):
    model = AudioDownload
    max_num = 1


class VideoDownloadInline(admin.StackedInline):
    model = VideoDownload
    max_num = 1


class ProductContributionInline(admin.StackedInline):
    model = ProductContribution
    extra = 0


class CatalogItemInline(admin.StackedInline):
    model = Item
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'ean', 'support_type', 'restriction', 'on_sale', 'flag',)
    list_filter = ( 'support_type', 'languages', 'on_sale', 'restriction', 'subject', ) #'languages__code'
    search_fields = ['title', 'authors',  'ean',  'code', 'ipc', 'subject__name',]
    raw_id_fields=('derivative', 'copyright_holder') 
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "languages":
             kwargs["queryset"] = Language.objects.all()
        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    inlines = [
        BookInline, eBookInline, CDInline, DVDInline, GameInline, AudioDownloadInline, VideoDownloadInline, ProductContributionInline, CatalogItemInline
    ]
    
    save_as = True

    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/media')
        js = [
              static_url+'tiny_mce/tiny_mce.js',
              static_url+'admin/js/product_admin.js',
              ]

    fieldsets = (
        (None, {
            'fields': ('support_type', #'derivative',                            'masterpiece',
                       ('copyright_holder', 'copyright_year'),
                       "project",
                       ('ean', 'code', 'ipc'),
                       ('on_sale', 'price', ),
                       'quantity',
                       'flag',
                       'observations',  )
        }),
        (None, {
            'fields': ('authors', 'title', 'subtitle',
                    ('is_translated', 'languages'),
                    ('subject','tags'),
                    'restriction',
                    'summary',
                    'description',
                    'image_name',
                )
        }),
        ("volumetry", {
            'fields': (
                    ( 'width', 'height', 'depth'),
                    'weight',
                )
        }),
    )


class EditionAdmin(admin.ModelAdmin):
    list_display = ('product', 'publisher', 'release_date')
    date_herarchy = ['release_date']
    list_filter = ('publisher__name', )
    search_fields = ['product__title', 'publisher__name']
    
    
admin.site.register(Language)
admin.site.register(Masterpiece)
admin.site.register(Product, ProductAdmin)
admin.site.register(Edition)

admin.site.register(Book)
# admin.site.register(CD)
# admin.site.register(DVD)
# admin.site.register(eBook)
# admin.site.register(Game)
# admin.site.register(Poster)
# admin.site.register(AudioDownload)
# admin.site.register(VideoDownload)

admin.site.register(Subject)
