# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
#
from catalogs.models import Item

PAYMEMNT_METHODS = (
    ("cash", "cash"),
    ("card", "card"),
)


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    total = models.DecimalField(max_digits=6, decimal_places=2,)
    paid = models.DecimalField(max_digits=6, decimal_places=2,)
    payment_method = models.CharField(max_length=6,
        choices=PAYMEMNT_METHODS,
        default="cash")
    observations = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s %s€ - %s" % (self.created, self.total, self.created_by)

  
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="related_orderitems",
        blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name="related_orderitems")
    quantity = models.SmallIntegerField("quantity",
        default=1)

    def __unicode__(self):
        return unicode(self.order)