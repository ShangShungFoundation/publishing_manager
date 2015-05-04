from django.db import models
from django.utils.translation import ugettext_lazy as _

ROLES = (
    (1, "translator"),
    (2, "transcriptor"),
    (3, "cover designer"),
    (4, "layout designer"),
    (5, "editor"),
    (6, "corrector"),
    (7, "photographer"),
    (8, "editing superviser"),
    (9, "project manager"),
    (10, "revisor"),
    (11, "performer"),
    (12, "collaborator"),
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
        return u"%s %s %s" % (self.product_id, self.get_role_display(), self.persona_id)


class Sponsorship(models.Model):
    """

    """
    product_id = models.ForeignKey("products.Product")
    persona_id = models.ForeignKey("persons.Persona")

    quantity = models.SmallIntegerField()
    description = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return u"%s sponsored by %s" % (self.product, self.persona)


class Project(models.Model):
    name = models.CharField(_(u'name'), max_length=32)
    description = models.TextField()

    def __unicode__(self):
        return self.name
