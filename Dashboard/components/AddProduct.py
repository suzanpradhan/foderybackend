import itertools
from django_unicorn.components import UnicornView
from django.utils.text import slugify
from Products.models import AttributeNames, Item, ItemCategory

class AddproductView(UnicornView):
    title = ""
    slug = ""
    productCategories = None
    variantAttributes = None
    selectedVariantAttributes = None
    attributeNameInput = ""

    def get_categories(self):
        self.productCategories = ItemCategory.objects.filter(status=True).all()

    def get_variantAttributeNames(self):
        print("here")
        self.variantAttributes = AttributeNames.objects.all()

    def mount(self):
        self.get_variantAttributeNames()

    def generate_slug(self):
        # max_length = Item._meta.get_field('slug').max_length
        # value = self.title
        slug_candidate = slug_original = slugify(self.title, allow_unicode=True)
        # for i in itertools.count(1):
            # if not Item.objects.filter(slug=slug_candidate).exists():
                # break
            # slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate
        slug_candidate = ""

    def addAttributeNameInput(self):
        if self.addAttributeNameInput != "":
            attribueObj = AttributeNames(title=self.attributeNameInput)
            attribueObj.save()
            self.addAttributeNameInput = ""
            self.get_variantAttributeNames()


