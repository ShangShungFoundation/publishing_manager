import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.conf import settings

from prestashop.models import PsCustomer, PsOrder
from catalogs.models import Item

from views import deliver


class Client(models.Model):
    """

    """
    name = models.CharField(_(u'name'), max_length=132)
    surname = models.CharField(_(u'surname'), max_length=132)
    password = models.CharField(blank=True, null=True, max_length=132)
    email = models.EmailField()

    customer = models.ForeignKey(
        PsCustomer,
        related_name="related_webshop_customers",
        blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="related_client_creators")

    def __unicode__(self):
        return (u"%s %s") % (self.name, self.surname)

    class Meta:
        unique_together = ("name", "surname", "email")

    def save(self, *args, **kwargs):
        if self.password == "":
            hsh = hashlib.sha224(u"%s%s" % (self.surname, settings.SECRET_KEY))
            self.password = hsh.hexdigest()[0:6]
        super(Client, self).save(*args, **kwargs)


class EProduct(models.Model):
    item = models.ForeignKey(
        Item,
        related_name="related_eproducts")

    def __unicode__(self):
        return self.item.__unicode__()


class Delivery(models.Model):
    client = models.ForeignKey(
        Client,
        related_name="related_delivery_clients")
    eproduct = models.ForeignKey(
        EProduct,
        related_name="related_eproducts")
    order = models.ForeignKey(
        PsOrder,
        related_name="related_orders",
        blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="related_delivery_creators")

    def __unicode__(self):
        return u"client #%s eproduct %s" % (self.client.id, self.eproduct.__unicode__())

    def clean(self):
        if not self.client.email:
            raise ValidationError('client must have email')

    def save(self, *args, **kwargs):
        if self.pk == None:
            product = self.eproduct.item.product
            delieverd = deliver(
                self.client.name,
                self.client.surname,
                self.client.email,
                product.ean,
                product.support_type)
        super(Delivery, self).save(*args, **kwargs)