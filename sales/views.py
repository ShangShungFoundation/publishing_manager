import json
import datetime
import dateutil.relativedelta
import csv

from django.utils import timezone
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required

from catalogs.models import Item

from models import Order, OrderItem
from products.models import Product
from prestashop.models import PsProduct
from prestashop.views import diminish_stock


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def respond_csv(data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ssi_stats.csv"'

    writer = csv.writer(response)
    #writer.writerow(u'\ufeff'.encode('utf8')) 
    for item in data:
        writer.writerow([smart_str(cell) for cell in item.values()])

    return response

#@login_required
def put_shop_order(request, shop_id):
    shop = User.objects.get(id=shop_id)
    items_str = request.REQUEST.getlist("items")

    if items_str:
        total = request.REQUEST.get("total")
        paid = request.REQUEST.get("paid")
        created_timestamp = request.REQUEST.get("created")
        created = timezone.datetime.fromtimestamp(int(created_timestamp[:10]))
        created_time = created.replace(tzinfo=timezone.utc)

        order = Order.objects.create(
            total=total,
            paid=paid,
            created_by_id=int(shop_id),
            created =created_time)
        
        for it in items_str:
            item = json.loads(it)[0]
            ean = item["ean"]
            quantity = int(item["quantity"])
            item = Item.objects.get(product__ean=ean, catalog_id=3)
            order_item=OrderItem(
                pk=None,
                order=order,
                item=item,
                quantity=quantity)
            order_item.save()

            # deminish stock quantity
            product = PsProduct.objects.get(ean13=ean)
            product.quantity = product.quantity - quantity
            product.save()
            product_stock = diminish_stock(product, quantity)

        response = HttpResponse(
            "[true]", content_type='application/json')
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
        response["Access-Control-Max-Age"] = "1000"  
        response["Access-Control-Allow-Headers"] = "*"  
        return response
    else:
        return render(request, "sales/order.html", {"shop":shop})


def get_shop_sales_by_month(shop_id):
    #http://stackoverflow.com/questions/8746014/django-group-sales-by-month
    from django.db import connection
    truncate_data = connection.ops.date_trunc_sql('month','created')
    qs = Order.objects.filter(created_by_id=shop_id).extra({'month':truncate_data })
    report = qs.values('month').annotate(Sum('paid'), Count('pk')).order_by('month')
    return report


def get_shop_sales_old(shop_id, year, month=None, day=None):
    #http://stackoverflow.com/questions/8746014/django-group-sales-by-month
    qs_dict = dict(
        order__created_by_id=shop_id,
        order__created__year=year
    )

    if month:
        qs_dict["order__created__month"]=month
    if day:
        qs_dict["order__created__day"]=day
    # TODO fix filtering for month, proppably mysql issue
    qs = OrderItem.objects.filter(**qs_dict)
    report = qs.values("item__product__title", "item__product__ean").annotate(Sum('quantity')).order_by("-quantity__sum")
    return report


def get_shop_sales(shop_id, year, month=None, day=None):
    #http://stackoverflow.com/questions/8746014/django-group-sales-by-month

    qs_dict = dict()

    if shop_id:
        qs_dict["order__created_by_id"] = shop_id

    default_tz = timezone.get_default_timezone()

    if day:
        this_day = datetime.datetime(int(year), int(month), int(day))
        prev_day = timezone.make_aware(this_day - datetime.timedelta(days = 1), default_tz)    
        next_day = timezone.make_aware(this_day + datetime.timedelta(days = 1), default_tz)   
        qs_dict["order__created__range"] = (prev_day, next_day)
    elif (not day and month):
        this_month = datetime.datetime(int(year), int(month), 1)
        prev_month = timezone.make_aware(this_month - datetime.timedelta(days = 1), default_tz)    
        next_month = this_month + datetime.timedelta(days = 35)
        next_month = timezone.make_aware(next_month.replace(day=1), default_tz)
        qs_dict["order__created__range"] = (prev_month, next_month)
    else:
        qs_dict["order__created__year"]=int(year)
    #import ipdb; ipdb.set_trace()

    # TODO fix filtering for month, proppably mysql issue
    qs = OrderItem.objects.filter(**qs_dict)
    report = qs.values("item__product__title", "item__product__ean").annotate(Sum('quantity')).order_by("-quantity__sum")
    return report


def get_shop_sales_for_dates(frm, to, shop_id=None):
    #http://stackoverflow.com/questions/8746014/django-group-sales-by-month
    qs_dict = dict()

    if shop_id:
        qs_dict["order__created_by_id"] = shop_id

    default_tz = timezone.get_default_timezone()

    date_from = datetime.datetime.strptime(frm, "%Y-%m-%d")
    date_to = datetime.datetime.strptime(to, "%Y-%m-%d")
    qs_dict["order__created__range"] = (date_from, date_to)
    
    #import ipdb; ipdb.set_trace()
    
    # TODO fix filtering for month, proppably mysql issue
    qs = OrderItem.objects.filter(**qs_dict)
    report = qs.values("item__product__title", "item__product__ean", "item__product__quantity", "item__product__price").annotate(Sum('quantity')).order_by("-quantity__sum")
    return report


@login_required
def get_month_stats(request, shop_id):
    shop = User.objects.get(id=shop_id)
    sales_by_month = get_shop_sales_by_month(shop_id)
    
    return render(request, "sales/sales_statistics.html", {"sales": sales_by_month, "shop":shop})
    

@login_required
def get_sales_stats(request, year, month_id=None, day=None):
    sales_by_month = get_shop_sales(None, year, month_id, day)
    if "output" in request.GET:
        return respond_csv(sales_by_month)
    else:
        return render(request, "sales/sales_items_stats.html", 
                  {"sales": sales_by_month,
                   "year":year,
                   "month":month_id})


@login_required
def get_sales_stats_for_period(request, frm, to, shop_id=None):
    sales = get_shop_sales_for_dates(frm, to, shop_id)
    if "output" in request.GET:
        return respond_csv(sales)
    else:
        return render(request, "sales/sales_stats_total.html", 
                  {"sales": sales,
                   "from":frm,
                   "to":to})
                  
                  
                  
@login_required
def get_shop_sales_stats(request, shop_id, year, month_id=None, day=None):
    x_forwarded_for = request.META.get('REMOTE_ADDR')
    
    
    
    shop = User.objects.get(id=shop_id)
    sales_by_month = get_shop_sales(shop_id, year, month_id, day)
    
    if "output" in request.GET:
        return respond_csv(sales_by_month)
    
    return render(request, "sales/sales_items_stats.html", 
                  {"sales": sales_by_month,
                   "shop":shop,
                   "year":year,
                   "month":month_id})

                  
@login_required
def get_year_sales_stats(request, shop_id, year):
    shop = User.objects.get(id=shop_id)
    
    sales_by_month = get_shop_sales(shop_id, year)
    return render(request, "sales/sales_items_stats.html", 
                  {"sales": sales_by_month,
                   "shop":shop,
                   "year":year})  
                  
def barcode_create(request):
    return render(request, "sales/barcode.html")  