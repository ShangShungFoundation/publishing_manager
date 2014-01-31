from django.db import models
from django.utils.translation import ugettext_lazy as _


class Persona(models.Model):
    """

    """
    name_surname = models.CharField(_(u'name'), max_length=32)
    email = models.EmailField()
    tel = models.CharField(
        _(u'tel'), max_length=32,
        blank=True, null=True)
    adress = models.TextField()
    country = models.CharField(max_length=50)

    observations = models.TextField()

    def __unicode__(self):
        return self.name_surname


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