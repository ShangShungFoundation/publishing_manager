from django.db import models
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    """

    """
    name = models.CharField(_(u'name'), max_length=32)
    email = models.EmailField()
    tel = models.CharField(
        _(u'name'), max_length=32,
        blank=True, null=True)
    adress = models.TextField()
    country = models.CharField(max_length=50)

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