from django.contrib import admin
from django.conf import settings

from models import Language, Masterpiece, Product, Edition, Book, CD, DVD, eBook, Game, Poster, AudioDownload, VideoDownload, Subject

from contributions.models import ProductContribution


class BookInline(admin.StackedInline):
    model = Book
    extra = 0


class eBookInline(admin.StackedInline):
    model = eBook
    extra = 0


class CDInline(admin.StackedInline):
    model = CD
    extra = 0


class DVDInline(admin.StackedInline):
    model = DVD
    extra = 0


class GameInline(admin.StackedInline):
    model = Game
    extra = 0


class AudioDownloadInline(admin.StackedInline):
    model = AudioDownload
    extra = 0


class VideoDownloadInline(admin.StackedInline):
    model = VideoDownload
    extra = 0

class ProductContributionInline(admin.StackedInline):
    model = ProductContribution
    extra = 0
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'masterpiece', 'ean', 'in_catalogue', 'support_type')
    list_filter = ('masterpiece', 'support_type', 'in_catalogue', 'on_sale' )
    search_fields = ['title', 'ean',  'code', 'ipc']
    
    inlines = [
        BookInline, eBookInline, CDInline, DVDInline, GameInline, AudioDownloadInline, VideoDownloadInline,
        ProductContributionInline
    ]
    save_as = True

    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/media')
        js = [static_url+'admin/js/product_admin.js']

    fieldsets = (
        (None, {
            'fields': ('support_type', 'derivative', 'masterpiece', 'ean', 'code', 'ipc', 'observations' )
        }),
        (None, {
            'fields': ('authors', 'title', 'subtitle',
                    ('is_translated', 'languages'),
                )
        }),
        ("volumetry", {
            'fields': (
                    ( 'width', 'height'),
                    'weight',
                )
        }),
         ("catalog", {
            'fields': (
                    ('in_catalogue', 'on_sale'),
                    'url'
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
admin.site.register(Edition, EditionAdmin)

# admin.site.register(Book)
# admin.site.register(CD)
# admin.site.register(DVD)
# admin.site.register(eBook)
# admin.site.register(Game)
# admin.site.register(Poster)
# admin.site.register(AudioDownload)
# admin.site.register(VideoDownload)

admin.site.register(Subject)
