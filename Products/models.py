
from django.db import models
from datetime import datetime
from django.db.models import base
from django.db.models.base import Model
from django.template.defaultfilters import slugify
from enum import Enum

from QuickOrder.models import Diet, FoodType

# from QuickOrder.models import Diet, FoodType


class Nutrition(models.Model):
    title = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    unit = models.CharField(null=True, blank=True, max_length=255)

    createdAt = models.DateField(auto_now=True)
    updatedAt = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):

        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


unitChoices = ((1, "g"), (2, "kg"), (3, "lbs"))


class ItemAttr(models.Model):
    weight = models.IntegerField(null=True, blank=True)
    unit = models.IntegerField(choices=unitChoices, default=1)

    length = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)


class ItemCategory(models.Model):
    title = models.TextField(blank=True)
    description = models.TextField(null=True, blank=True)
    isFeatured = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    coverImage = models.ForeignKey(
        "General.MediaFile",
        verbose_name=("item_category_cover_image"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    createdAt = models.DateField(auto_now=True)
    updatedAt = models.DateField(null=True, blank=True)

    isParent = models.BooleanField(default=False)
    parentId = models.ForeignKey(
        "self",
        verbose_name=("item_category_item_category_relation"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class ExtraGroup(models.Model):
    title = models.TextField(null=True, blank=True)

    createdAt = models.DateField(auto_now=True)
    updatedAt = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):

        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class Extra(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(null=True, unique=True)

    coverImage = models.ForeignKey(
        "General.MediaFile",
        verbose_name=("extra_cover_image"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    createdAt = models.DateField(auto_now=True)
    updatedAt = models.DateField(null=True, blank=True)

    extraGroup = models.ForeignKey(
        ExtraGroup,
        verbose_name=("extra_extra_group_relation"),
        on_delete=models.CASCADE,
        blank=True,null=True
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):

        self.updated_at = datetime.now()
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class AttributeItem(models.Model):
    title = models.TextField(blank=True)
    coverImage = models.ForeignKey(
        "General.MediaFile", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.title


class AttributeNames(models.Model):
    title = models.TextField(blank=True)

class Attribute(models.Model):
    item = models.ForeignKey("Products.Item", on_delete=models.CASCADE, null=True)
    name = models.ForeignKey(AttributeNames, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(AttributeItem, blank=True)

    def __str__(self) -> str:
        string = ""
        string = string + (self.item.title if self.item else "") + "-"
        string += self.name.title if self.name else str(self.id)
        return string

    def readable_name(self):
        return self.name.title if self.name else str(self.id)

class VariantItem(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True)
    attributeItem = models.ForeignKey(AttributeItem, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.attribute.__str__() + "-" + self.attributeItem.title if self.attribute and self.attributeItem else str(self.id)

    def readable_name(self):
        return self.attribute.readable_name() + " : " + self.attributeItem.title if self.attribute and self.attributeItem else str(self.id)

class Variant(models.Model):
    price = models.FloatField(null=True, blank=True)
    items = models.ManyToManyField(VariantItem, blank=True)

    def __str__(self) -> str:
        string = ""
        if self.items:
            for i in self.items.all():
                string = string + "-" + i.__str__()
        else:
            string = self.id
        return string

    def readable_name(self):
        tempName = ""
        if self.items:
            for i, element in enumerate(self.items.all()):
                if (i == (self.items.count() - 1)):
                    tempName = tempName + element.readable_name() 
                else:
                    tempName = tempName + element.readable_name() + " /"
        else:
            string = self.id
        return tempName
                

class Item(models.Model):
    title = models.TextField(blank=True)
    description = models.TextField(null=True, blank=True)
    isFeatured = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    isDeliverable = models.BooleanField(default=False)
    newPrice = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    slug = models.SlugField(null=True, unique=True,blank=True)
    avgRating = models.IntegerField(default=0)
    servings = models.IntegerField(default=1)
    createdAt = models.DateField(auto_now=True)
    updatedAt = models.DateField(null=True, blank=True)

    itemAttribute = models.ForeignKey(
        ItemAttr,
        verbose_name=("item_item_attr"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        ItemCategory,
        verbose_name=("item_cat_item_relation"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    relatedProduct=models.ManyToManyField(
        'self', blank=True
    )

    nutritions = models.ManyToManyField(Nutrition, blank=True)

    extra = models.ManyToManyField(Extra, blank=True)

    variant = models.ManyToManyField(Variant, blank=True)

    packageCount = models.IntegerField(null=True, blank=True)

    coverImage = models.ForeignKey(
        "General.MediaFile",
        related_name=("item_cover_image"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    gallery = models.ManyToManyField(
        "General.MediaFile", verbose_name=("item_gallery_images"), blank=True
    )

    diets = models.ManyToManyField(Diet, blank=True)
    foodTypes = models.ManyToManyField(FoodType, blank=True)
    tax = models.ForeignKey(
        "Settings.Tax",
        verbose_name=("item_tax"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.updated_at = datetime.now()
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def attributes(self):
        x = [[Attribute.objects.get(id=j.attribute.id) for j in i.items.all()] for i in self.variant.all()]
        return x[0] if len(x) > 0 else None


class Favorite(models.Model):
    user = models.ForeignKey("CustomUser.UserProfile", on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    isLiked = models.BooleanField(default=False)


class Collection(models.Model):
    title = models.TextField(blank=True)
    description = models.TextField(null=True, blank=True)
    isFeatured = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    foods = models.ManyToManyField(Item)
    slug = models.SlugField()

    coverImage = models.ForeignKey(
        "General.MediaFile",
        verbose_name=("item_category_cover_image"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    createdAt = models.DateField(auto_now=True)
    updatedAt = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

class OfferChoice(Enum):
    percentage = 1
    amount = 2


class Offers(models.Model):
    title = models.TextField(blank=True)
    coverImage = models.ForeignKey("General.MediaFile", on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT, blank=True, null=True)
    typeOfOffer = models.IntegerField(choices=((choice.value, choice.name) for choice in OfferChoice),default=1)
    value = models.FloatField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    endAt = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
    