import pycountry

from django.db import models
from django.utils.translation import ugettext_lazy as _

COUNTRIES = [[c.alpha2, c.name] for c in pycountry.countries]

class Persona(models.Model):
    """

    """
    name_surname = models.CharField(_(u'name'), max_length=32)
    email = models.EmailField(
        blank=True, null=True)
    tel = models.CharField(
        _(u'tel'), max_length=32,
        blank=True, null=True)
    adress = models.TextField(
        blank=True, null=True)
    country = models.CharField(
        max_length=3, choices=COUNTRIES, default="IT" )

    observations = models.TextField(
        blank=True, null=True)

    def __unicode__(self):
        return self.name_surname

    class Meta:
        ordering = ["name_surname"]
        
        
class Author(models.Model):
    name = models.CharField(_(u'name'), max_length=32)
    surname = models.CharField(_(u'surname'), max_length=32)
    initials = models.SlugField()

    biography = models.TextField()

    class Meta:
        verbose_name = _(u"author")
        verbose_name_plural = _(u"authors")

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)

    @models.permalink
    def get_absolute_url(self):
        return ('state_list', [])