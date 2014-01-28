from django.db import models
from django.utils.translation import ugettext_lazy as _

from persons.models import Persona
from partners.models import Company


class Subject(models.Model):
    name = models.CharField(_(u'name'), max_length=32)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(_(u'name'), max_length=32)
    code = models.CharField(_(u'code'), max_length=3)

    def __unicode__(self):
        return self.name


RESTRICTION_LEVELS = (
    ("public", _("public")),
    ("introduction", _("Dzogchen introduction needed")),
    ("transmition", _("transmition needed")),
    ("sms", _("SMS only")),
)


class Masterpiece(models.Model):
    authors = models.ManyToManyField("persons.Author")

    title = models.CharField(max_length=232)
    subtitle = models.CharField(max_length=232)
    language = models.ForeignKey(Language, verbose_name=_(u'original language'))
    copyright_holder = models.ForeignKey(Persona)
    first_edition_year = models.SmallIntegerField(
        _("first edition year"), max_length=4)
    last_edition_year = models.SmallIntegerField(
        _("last edition year"), max_length=4,
        blank=True,  null=True)
    subject = models.ForeignKey(Subject)

    restriction = models.CharField(_("restiction level"),
            choices=RESTRICTION_LEVELS, max_length=50)

    class Meta:
        verbose_name = _(u"masterpiece")
        verbose_name_plural = _(u"masterpieces")

    def __unicode__(self):
        auhors = self.authors
        return "%s - %s" % (auhors, self.title)


SUPPORT_TYPES = (
    ("book", "Book"),
    ("ebook", "eBook"),
    ("cd", "CD"),
    ("dvd", "DVD"),
    ("poster", "Poster"),
    ("game", "Game"),
    ("audiodownload", "Audio download"),
    ("videodownload", "Video download"),
    ("comp", "Composed product"),
)


class Product(models.Model):
    """

    """
    masterpiece = models.ForeignKey(Masterpiece)
    ean = models.CharField("EAN/ISBN", max_length=16, blank=True,  null=True)
    code = models.CharField(max_length=50, blank=True,  null=True)
    ipc = models.CharField("IPC", max_length=50, blank=True,  null=True)
    derivative = models.ForeignKey("Product",
        help_text="in the case if product derivate from other product",
        blank=True, null=True)

    authors = models.CharField("Author/s", max_length=256)
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256, blank=True,  null=True)

    contributions = models.ManyToManyField(Persona,
        through='contributions.ProductContribution')
    project = models.ForeignKey('contributions.Project',
        blank=True,  null=True)

    languages = models.ManyToManyField(Language, verbose_name=u'languages')
    is_translated = models.BooleanField(_("is translated"))

    weight = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)

    url = models.URLField("webshop page", blank=True,  null=True,
        help_text="webshop product url")
    in_catalogue = models.BooleanField(_("in catalogue"))
    on_sale = models.BooleanField(_("in sale"))

    support_type = models.CharField(_("support type"),
        choices=SUPPORT_TYPES, max_length=15)

    observations = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return "%s - %s" % (self.ean, self.title)


class Edition(models.Model):
    """

    """
    publisher = models.ForeignKey(Company, related_name="related_publishers")
    product = models.ForeignKey(Product)

    release_date = models.DateField()
    quantity = models.SmallIntegerField()

    price_brutto = models.DecimalField(max_digits=5, decimal_places=2)
    price_netto = models.DecimalField(max_digits=5, decimal_places=2)
    copy_price_netto = models.DecimalField(max_digits=5, decimal_places=2)
    copy_price_brutto = models.DecimalField(max_digits=5, decimal_places=2)
    vat = models.DecimalField(max_digits=5, decimal_places=2)

    observations = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return "%s - %s" % (self.product, self.release_date)


PAPER_FINISH = (
    (1, "coated"),
    (2, "uncoated"),
)


class Book(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    reading_line = models.CharField(max_length=256, blank=True,  null=True)
    chapters = models.TextField()

    cover_colors = models.CharField(max_length=20,
        help_text="CMYK + Pantone colours")
    cover_paper_name = models.CharField(max_length=40, blank=True,  null=True)
    cover_paper_gramature = models.SmallIntegerField(max_length=40,
        blank=True,  null=True)
    cover_paper_finish = models.SmallIntegerField(
        max_length=40, choices=PAPER_FINISH,
        blank=True,  null=True)
    cover_paper_ornaments = models.TextField(blank=True, null=True)

    bw_pages_nr = models.IntegerField(default=0)
    bw_paper_name = models.CharField(max_length=40, blank=True,  null=True)
    bw_paper_gramature = models.SmallIntegerField(max_length=40,
        blank=True, null=True)

    color_pages_nr = models.IntegerField(default=0)
    color_paper_name = models.CharField(max_length=40, blank=True,  null=True)
    color_paper_gramature = models.SmallIntegerField(
        max_length=40, blank=True, null=True)

    observations = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return "%s" % (self.product)


CD_MEDIA = (
    ("audio", "audio"),
    ("mp3", "mp3"),
)


class CD(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    songs = models.TextField()
    duration = models.SmallIntegerField(help_text="in minutes")
    media_format = models.CharField(choices=CD_MEDIA, max_length=20)

    def __unicode__(self):
        return "CD %s" % (self.product)


DVD_SYSTEM = (
    ("pal", "PAL"),
    ("ntsc", "NTSC"),
)

DVD_MEDIA = (
    ("mp4", "mp4"),
    ("ntsc", "ntsc"),
)


class DVD(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    chapters = models.TextField()
    duration = models.SmallIntegerField(help_text="in minutes")
    media_format = models.CharField(choices=DVD_MEDIA, max_length=20)
    media_format = models.CharField(choices=DVD_SYSTEM, max_length=20)

    def __unicode__(self):
        return "DVD %s" % (self.product)


class Poster(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    colors = models.CharField(max_length=40)
    paper_name = models.CharField(max_length=40)
    paper_gramature = models.SmallIntegerField(max_length=40)

    def __unicode__(self):
        return "Poister %s" % (self.product)


class Game(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    characteristics = models.TextField()

    def __unicode__(self):
        return "Game %s" % (self.product)


class eBook(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    chapters = models.TextField()
    pages_nr = models.IntegerField(default=0)
    size = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="in Mb")

    def __unicode__(self):
        return "eBook %s" % (self.product)


AUDIO_FORMAT = (
    (1, "mp3"),
)


class AudioDownload(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    files = models.TextField()
    size = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="in Mb")
    format = models.SmallIntegerField(choices=AUDIO_FORMAT, default=1)

    def __unicode__(self):
        return "Audio Download %s" % (self.product)


VIDEO_FORMAT = (
    (1, "mp4"),
)


class VideoDownload(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    files = models.TextField()
    size = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="in Mb")
    format = models.SmallIntegerField(choices=VIDEO_FORMAT, default=1)

    def __unicode__(self):
        return "Video Download %s" % (self.product)
