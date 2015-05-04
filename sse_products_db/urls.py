from django.conf.urls import patterns, include, url
from wiki.urls import get_pattern as get_wiki_pattern
from django_notify.urls import get_pattern as get_notify_pattern

from django.conf import settings

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sse_products_db.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'lib.admin_csv_export.admin_list_export'),
    
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^catalogs/', include("catalogs.urls")),
    (r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    (r'^accounts/', include('allauth.urls')),
    (r'^sales/', include('sales.urls')),
    (r'^notify/', get_notify_pattern()),
    (r'wiki', get_wiki_pattern()),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
