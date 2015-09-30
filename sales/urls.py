from django.conf.urls import patterns, url

urlpatterns = patterns('sales.views',
    url(r'^barcode/$', "barcode_create", name='barcode_create'),
    url(r'^statistics/(?P<frm>.+)/(?P<to>.+)/$', "get_sales_stats_for_period", name='sales_stats_for_time'),
    url(r'^shop/statistics/(?P<year>\d+)/$', "get_sales_stats", name='sales_year_stats'),
    url(r'^shop/statistics/(?P<year>\d+)/(?P<month_id>\d+)/$', "get_sales_stats", name='sales_stats'),
    url(r'^shop/(?P<shop_id>\d+)/order/$', "put_shop_order", name='put_shop_order'),
    url(r'^shop/(?P<shop_id>\d+)/statistics/(?P<year>\d+)/(?P<month_id>\d+)/(?P<day>\d+)/$', "get_shop_sales_stats", name='sales_shop_day_stats'),
    url(r'^shop/(?P<shop_id>\d+)/statistics/(?P<year>\d+)/(?P<month_id>\d+)/$', "get_shop_sales_stats", name='sales_shop_stats'),
    url(r'^shop/(?P<shop_id>\d+)/statistics/(?P<year>\d+)/$', "get_year_sales_stats", name='sales_shop_year_stats'),
    url(r'^shop/(?P<shop_id>\d+)/statistics/$', "get_month_stats", name='sales_shop_month_stats'),
)
