from django.contrib import admin
from django.conf import settings

from models import Language, Masterpiece, Product, Edition, Book, CD, DVD, eBook, Game, Poster, AudioDownload, VideoDownload, Subject


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


class ProductAdmin(admin.ModelAdmin):
    model = VideoDownload
    list_display = ('masterpiece', 'ean', 'title', 'in_catalogue')
    inlines = [
        BookInline, eBookInline, CDInline, DVDInline, GameInline, AudioDownloadInline, VideoDownloadInline
    ]


    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/media')
        js = [static_url+'admin/js/product_admin.js']

    fieldsets = (
        (None, {
            'fields': ('masterpiece', 'ean', 'code', 'ipc', 'derivative', 'support_type')
        }),
        (None, {
            'fields': ('authors', 'title', 'subtitle',
                    ('is_translated', 'languages'),
                )
        }),
        ("volumetry", {
            'fields': (
                    ('length', 'width', 'height'),
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


admin.site.register(Language)
admin.site.register(Masterpiece)
admin.site.register(Product, ProductAdmin)
admin.site.register(Edition)

# admin.site.register(Book)
# admin.site.register(CD)
# admin.site.register(DVD)
# admin.site.register(eBook)
# admin.site.register(Game)
# admin.site.register(Poster)
# admin.site.register(AudioDownload)
# admin.site.register(VideoDownload)

admin.site.register(Subject)
