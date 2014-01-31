from django.db import models
from django.utils.translation import ugettext_lazy as _


ROLES = (
    (1, "translator"),
    (3, "designer"),
    (4, "editor"),
    (5, "corrector"),
    (6, "photographer"),
    (7, "colaborator"),
)


class ProductContribution(models.Model):
    """

    """
    product_id = models.ForeignKey("products.Product")
    persona_id = models.ForeignKey("persons.Persona")

    role = models.SmallIntegerField(choices=ROLES)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return "%s %s %s" % (self.product_id, self.get_role_display(), self.persona_id)


class Sponsorship(models.Model):
    """

    """
    product_id = models.ForeignKey("products.Product")
    persona_id = models.ForeignKey("persons.Persona")

    quantity = models.SmallIntegerField()
    description = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return "%s sponsored by %s" % (self.product, self.persona)


class Project(models.Model):
    name = models.CharField(_(u'name'), max_length=32)
    description = models.TextField()

    def __unicode__(self):
        return self.name
