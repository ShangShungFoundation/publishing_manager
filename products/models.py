from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from persons.models import Persona
from partners.models import Company
from prestashop.models import PsCategory, PsProduct


from django.conf import settings

from prestashop.conv_data import prepare_data
from prestashop.views import add_product, update_product, delete_product


class Subject(models.Model):
    """
    
    """
    name = models.CharField(_(u'name'), max_length=32)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey("Subject",
        blank=True, null=True)
    
    def show(self):
        if self.belongs_to_id:
            return u" > ".join([unicode(self.belongs_to), self.name])
        else:
            return self.name
        
    def __unicode__(self):
         return self.show()
    

    class Meta:
        ordering = ["-id"]
        

class Language(models.Model):
    code = models.CharField(_(u'name'), choices=settings.APP_LANGUAGES, max_length=32, unique=True)

    def __unicode__(self):
        return "%s - %s" % (self.code, self.get_code_display())

    class Meta:
        ordering = ["code"]
        

RESTRICTION_LEVELS = (
    ("public", _("public")),
    ("introduction", _("Dzogchen introduction needed")),
    ("transmition", _("Particular transmition needed")),
    ("sms0", _("SMS Base")),
    ("sms1", _("SMS 1st Level")),
    ("sms2", _("SMS 2nd Level")),
)


class Masterpiece(models.Model):
    """
    Related to original copy or Master. For example it is original from which difrent translations are done.
    Another feature is describing intelectual authorship.
    """
    authors = models.ManyToManyField("persons.Author")

    title = models.CharField(max_length=232)
    subtitle = models.CharField(max_length=232,
        blank=True,  null=True)
    language = models.CharField(max_length=5, choices=settings.APP_LANGUAGES)
    copyright_holder = models.ForeignKey(Persona)

    restriction = models.CharField(_("restiction level"),
            choices=RESTRICTION_LEVELS, max_length=50)

    class Meta:
        verbose_name = _(u"master")
        verbose_name_plural = _(u"master")

    def __unicode__(self):
        #auhors = self.authors
        return self.title


SUPPORT_TYPES = (
    ("book", "Book"),
    ("ebook", "eBook"), 
    ("cd", "CD"),
    ("dvd", "DVD"),
    ("poster", "Poster"),
    ("game", "Game"),
    ("audiodownload", "Audio download"),
    ("videodownload", "Video download"),
    ("med", "Medicine"),
    ("accessories", "Accessories"),
    ("comp", "Composed product"),
)


class Product(models.Model):
    """
    Defines particular product. There can be situations that practically the same book may apear as diferent product becouse of difrent binding etc.
    """
    tags = TaggableManager()
    
    ean = models.CharField("EAN/ISBN", max_length=26, blank=True,  null=True)
    code = models.CharField(max_length=50, blank=True,  null=True)
    ipc = models.CharField("IPC", max_length=50, blank=True,  null=True)
    derivative = models.ForeignKey("Product",
        help_text="in the case if product derivate from other product",
        blank=True, null=True)

    authors = models.CharField("Author/s", 
	max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256, blank=True,  null=True)
    
    masterpiece = models.ForeignKey(Masterpiece,
        blank=True, null=True)
    
    copyright_holder = models.ForeignKey(Persona,
        related_name="related holders",
        blank=True, null=True, )
    copyright_year = models.SmallIntegerField(max_length=4,
        blank=True, null=True)
    
    
    summary = models.TextField(
        blank=True,  null=True,
        help_text="temporarly is here finally it should go to the masterpiece")
    description = models.TextField(
        #blank=True,  null=True,
        help_text="temporarly is here finally it should go to the masterpiece")
        
    contributions = models.ManyToManyField(Persona,
        through='contributions.ProductContribution')
    project = models.ForeignKey('contributions.Project',
        blank=True, null=True)

    languages = models.ManyToManyField(Language, verbose_name=u'languages')
    is_translated = models.BooleanField(_("is translated"))

    weight = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True,
        help_text="in Kg")
    width = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True,
        help_text="in Cm")
    height = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True,
        help_text="in Cm")
    depth = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True,
        help_text="in Cm")
    
    #in_catalogue = models.BooleanField(_("in catalogue"))
    on_sale = models.BooleanField(_("on sale"))
    # TODO temporarly price is here finally it should go to the edition
    price = models.DecimalField(_("recommended price"),
        max_digits=5, decimal_places=2,
        blank=True,  null=True,
        help_text="in Euro. temporarly price is here finally it should go to the edition")
    
    support_type = models.CharField(_("support type"),
        choices=SUPPORT_TYPES, max_length=25)

    observations = models.TextField(blank=True,  null=True)
    flag = models.BooleanField("status", default=False,
        help_text="if its 'off' - the product requires attention.Put more details in 'observations'")

    restriction = models.CharField(_("restiction level"),
            choices=RESTRICTION_LEVELS, max_length=50)
        
    first_edition_year = models.CharField(
        _("first edition year"), max_length=20,
        blank=True,  null=True)
    last_edition_year = models.CharField(
        _("last edition year"), max_length=20,
        blank=True,  null=True)
    
    subject = models.ForeignKey(Subject)
    #webshop_cat = models.ForeignKey(PsCategory)
    
    quantity = models.IntegerField(
        _("stock quantity"),
        blank=True,  null=True)
    
    image_name = models.ImageField(_("image name"),
        upload_to="product_images/",
        max_length=200,
        blank=True,  null=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.ean, self.title)

    def save(self, *args, **kwargs):
        
        if self.pk is None:
            # incerase weight for new items for 15%
            if self.weight:
                weight = float(self.weight)
                self.weight = weight + (weight * 0.15)
        else:
            prepared_data = prepare_data(self)
            from catalogs.models import Item
            catalog_item = Item.objects.filter(product=self, catalog_id=3)
            if len(catalog_item) == 1:
                
                try:
                    ps_product = PsProduct.objects.get(ean13=prepared_data["ean13"])
                except PsProduct.DoesNotExist:
                    pass
                else:
                    ps_product = update_product(ps_product, prepared_data)
        super(Product, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        ean = self.ean
        super(Product, self).delete(*args, **kwargs)
        try:
            delete_product(ean)
        except:
            pass


class Edition(models.Model):
    """
    
    """
    publisher = models.ForeignKey(Company, related_name="related_publishers")
    product = models.ForeignKey(Product, related_name="related_editions")
    release_date = models.DateField()
    quantity = models.SmallIntegerField("edition quantity",
        blank=True, null=True,
        help_text="if blank it is edition is considered to be released on demand")

    cost = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)
    copy_cost = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)
        
    price = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)
    copy_price = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)
        
    vat = models.DecimalField(max_digits=5, decimal_places=2,
        blank=True,  null=True)

    observations = models.TextField(blank=True,  null=True)

    def __unicode__(self):
        return "%s - %s" % (self.product, self.publisher)


PAPER_FINISH = (
    (1, "coated"),
    (2, "uncoated"),
)


class Book(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    reading_line = models.CharField(max_length=256, blank=True,  null=True)
    chapters = models.TextField("Contents", 
        blank=True,  null=True)

    cover_colors = models.CharField(max_length=20,
        help_text="CMYK + Pantone colors ex.: 4/0")
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

    observations = models.TextField(blank=True, null=True)

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
    songs = models.TextField("tracks", 
         blank=True,  null=True)
    duration = models.SmallIntegerField(
        help_text="in minutes",
        blank=True,  null=True)
    media_format = models.CharField(choices=CD_MEDIA, max_length=20)

    def __unicode__(self):
        return "CD %s" % (self.product)


DVD_SYSTEM = (
    ("pal", "PAL"),
    ("ntsc", "NTSC"),
    ("mp4", "mp4"),
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
    duration = models.SmallIntegerField(
        help_text="in minutes",
        blank=True,  null=True)
    media_format = models.CharField(choices=DVD_MEDIA, max_length=20)
    media_format = models.CharField(choices=DVD_SYSTEM, max_length=20)

    def __unicode__(self):
        return "DVD %s" % (self.product)


class Medicine(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    packaging = models.TextField()

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

EBOOK_FORMAT = (
    (1, "pdf"),
    (2, "ePub"),
    (3, "kindle"),
)

class eBook(models.Model):
    """

    """
    product = models.ForeignKey(Product)
    chapters = models.TextField(blank=True, null=True)
    pages_nr = models.IntegerField(default=0)
    format = models.SmallIntegerField(default=0, choices=EBOOK_FORMAT)
    file  = models.FileField(upload_to="product_ebooks/",
           blank=True,  null=True)
    size = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
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
    file  = models.FileField(upload_to="product_mp3/",
        blank=True,  null=True)
    duration = models.SmallIntegerField(
        help_text="in minutes",
        blank=True,  null=True)

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
    file  = models.FileField(upload_to="product_videos/",
        blank=True,  null=True)
    duration = models.SmallIntegerField(
        help_text="in minutes",
        blank=True,  null=True)

    def __unicode__(self):
        return "Video Download %s" % (self.product)
