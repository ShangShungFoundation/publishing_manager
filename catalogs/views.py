import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from models import Item

def items_json(request, catalog_id):
    #network = Network.objects.get(id=network_id)
    items = Itema.objects.all()
    return HttpResponse(items, mimetype='application/json')