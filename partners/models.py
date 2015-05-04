import pycountry

from django.db import models
from django.utils.translation import ugettext_lazy as _

COUNTRIES = [[c.alpha2, c.name] for c in pycountry.countries]

ACTIVITIES = (
    (1, "Print"),
    (2, "Publishing"),
    (3, "Dystribution"),
)

class Company(models.Model):
    """

    """
    name = models.CharField(_(u'name'), max_length=32)
    email = models.EmailField()
    
    tel = models.CharField(
        _(u'name'), max_length=32,
        blank=True, null=True)
    adress = models.TextField()
    country = models.CharField(
        max_length=3, choices=COUNTRIES, default="IT" )
    
    activity = models.SmallIntegerField(choices=ACTIVITIES)
    is_active = models.BooleanField(default=True)
    
    observations = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Company")
        verbose_name_plural = _(u"Companies")


class Distribution(models.Model):
    company_id = models.ForeignKey(Company)
    edition_id = models.ForeignKey("products.Edition")
    date_signed = models.DateField()
    quantity = models.SmallIntegerField()
    area = models.TextField()
    active = models.BooleanField()
    observations = models.TextField(blank=True,  null=True)
    
    def __unicode__(self):
        return self.company_id