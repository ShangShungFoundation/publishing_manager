import json
import decimal

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from models import Item
from products.models import Product


def items_json(request, catalog_id):
    products = Product.objects.filter(related_products__catalog_id__exact=catalog_id) 
    #products = Item.objects.select_related("product").filter(catalog_id__exact=catalog_id)

    products_json = serializers.serialize("json", products) #fields=('product','price')
    #import ipdb; ipdb.set_trace()
<<<<<<< HEAD
    
    return HttpResponse("importProducts(%s)" % products_json,
        mimetype='application/json')
=======

    return HttpResponse("importProducts(%s)" % products_json,
        content_type='application/json')
>>>>>>> a519447fd270393bc5bb2997dd8805020517c3f6
