# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from partners.models import Company
from products.models import Product, Edition

from prestashop.conv_data import prepare_data
from prestashop.views import add_product, reindex_products


CURRENCIES = (
    ("euro", u"€"),
    ("dolar", u"$"),
)


class Catalog(models.Model):
    name = models.CharField(_(u'name'), max_length=32)
    web = models.URLField("webshop page", blank=True,  null=True,
        help_text="webshop product url")
    is_active = models.BooleanField(default=True,)
    observations = models.TextField(blank=True, null=True)
    publisher = models.ForeignKey(Company, related_name="related_catalog")
    currency = models.CharField("default currency",
        choices=CURRENCIES,
        max_length=7, default="euro")

    def __unicode__(self):
        return self.name


class Item(models.Model):
    catalog = models.ForeignKey(Catalog, 
        related_name="related_items")
    product = models.ForeignKey(Product, related_name="related_products")
    #edition = models.ForeignKey(Edition, related_name="related_items",
    #    blank=True, null=True,)

    url = models.URLField("product url", blank=True,  null=True,
        help_text=" product url")
    catalog_code = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,)
    observations = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.product)

    def save(self, *args, **kwargs):
        if self.pk is None and self.catalog_id == 3:
            prepared_data = prepare_data(self.product)
            ps_product = add_product(prepared_data)
            #url = 
            self.catalog_code = ps_product.id_product
            self.price = ps_product.price
            #import ipdb; ipdb.set_trace()
        super(Item, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ean = self.product
        super(Item, self).delete(*args, **kwargs)
        delete_product(ean)