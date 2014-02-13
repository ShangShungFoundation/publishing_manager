import csv, decimal
from django.core.management.base import BaseCommand

from products.models import Product, Language
from persons.models import Persona
from contributions.models import ProductContribution
from catalogs.models import Catalog, Item

def set_colaboration(product, colaborator, role, desc=None):
    #import ipdb; ipdb.set_trace()
    persona, created = Persona.objects.get_or_create(name_surname=colaborator.strip())
    contribution = ProductContribution(
        product_id=product,
        persona_id=persona,
        role=role,
        description=desc
    )
    contribution.save()

sse_catalog = Catalog.objects.get(pk=1)

def importer(row):
    """SKU support language    public  title   EAN quantity    weight  summary description image   price   author  traduttore dal tibetano 1   traduttore dal tibetano 2   traduttore dal tibetano 3   1^ year pub.    anno di pubblicazione   Editor  Transcription by    en_translation  It_translation  note    Column"""
    
    product_dict = dict(
        ean=row[5],
        support_type=row[1],
        restriction=row[3],
        title=row[4],
        code=row[0],
        quantity=int(row[6] or 0),
        weight=decimal.Decimal(row[7] or "0"),
        summary=row[8],
        description=row[9],
        image_name=row[10],
        price=decimal.Decimal(row[11] or "0"),
        observations=row[22],
        is_translated=(row[13] or False),
        on_sale=(row[5] or False),
    )
    
    if row[12]:
        product_dict["authors"] = row[12]
    if row[16]:
        product_dict["first_edition_year"] = row[16]
    if row[17]:
        product_dict["last_edition_year"] = row[17]
    
    product = Product(**product_dict)
    product.save()
    
    if row[2]:
        for lang in row[2].split(","):
            ln = Language.objects.get(code=lang.strip().lower())
            product.languages.add(ln)
    
    if row[18]:
        for col in row[18].split(","):
            set_colaboration(product, col, 5) #editor
    if row[19]:
        for col in row[19].split(","):
            set_colaboration(product, col, 2) #transcription
    if row[20]:
        for col in row[20].split(","):
            set_colaboration(product, col, 1, "Translation to English")
    if row[21]:
        for col in row[21].split(","):
            set_colaboration(product, col, 1, "Translation to Italian")
            
    if row[13]:
        set_colaboration(product, row[13], 1, "Translation from Tibetan")
    if row[14]:
        set_colaboration(product, row[14], 1, "Translation from Tibetan")
    if row[15]:
        set_colaboration(product, row[15], 1, "Translation from Tibetan")

    if row[24]:
        item_dict = dict(
            catalog=sse_catalog,
            product=product,
            url="http://www.shangshungstore.org/index.php?l=product_detail&p=%s" % row[24],
            catalog_code=row[24],
            price=decimal.Decimal(row[11] or "0"),
        )
        item = Item(**item_dict)
        item.save()
    #product.m2m.save()

def import_csv(path, importer):
    with open(path) as f:
        reader = csv.reader(f)
        reader.next() # we skip first row with headers
        for row in reader:
            importer(row)


class Command(BaseCommand):
    help = "Import products from csv file"

    def execute(self, *args, **options):
        if len(args) == 1:
            path = args[0]
        import_csv(path, importer)


