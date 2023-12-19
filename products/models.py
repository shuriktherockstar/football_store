import os

from PIL import Image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from transliterate import translit

from products.enums import *
from users.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, editable=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, editable=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, editable=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class League(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, editable=False, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} {self.country}'

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(translit(self.name, 'ru', reversed=True))}-{slugify(translit(self.country.name, 'ru',reversed=True))}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Лига"
        verbose_name_plural = "Лиги"


class Club(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"


class Product(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=255, choices=Material.get_choices())
    sex = models.CharField(max_length=255, choices=Sex.get_choices())
    color = models.CharField(max_length=255, choices=Color.get_choices())
    slug = models.SlugField(blank=True, editable=False, unique=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='product_thumbnails/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.club}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(translit(f'{self.name} {self.club}', 'ru', reversed=True))

            self.image.name = f'{self.slug}.png'
            super().save(*args, **kwargs)

            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            thumbnail_path = os.path.join(settings.MEDIA_ROOT,
                                          f'product_thumbnails/{self.slug}_thumbnail.png')
            with Image.open(image_path) as img:
                img.thumbnail((50, 50))
                img.save(thumbnail_path, 'png')

            self.thumbnail.name = f'product_thumbnails/{self.slug}_thumbnail.png'

        else:
            old_product = Product.objects.get(pk=self.pk)
            if self.image != old_product.image:
                self.image.name = f'{self.slug}.png'
                super().save(*args, **kwargs)

                image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
                thumbnail_path = os.path.join(settings.MEDIA_ROOT, f'product_thumbnails/{self.slug}_thumbnail.png')

                with Image.open(image_path) as img:
                    img.thumbnail((50, 50))
                    img.save(thumbnail_path, 'png')

                self.thumbnail.name = f'product_thumbnails/{self.slug}_thumbnail.png'

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        properties = self.productunitproperty_set.all()
        property_values = ', '.join([f'{prop.property.name}: {prop.property_value}' for prop in properties])

        return f'{self.product}. {property_values}'

    class Meta:
        verbose_name = "Единица товара"
        verbose_name_plural = "Единицы товаров"
        unique_together = ('product', 'quantity')


class Property(models.Model):
    name = models.CharField(max_length=255)
    choices = models.CharField(max_length=255, choices=BaseProperty.get_subclasses(), default='Нет')

    def __str__(self):
        return self.name

    def get_property_values_for_product(self, product: Product):
        product_units = product.productunit_set.all().filter(quantity__gt=0)
        values_dict = {}

        for product_unit in product_units:
            try:
                value = ProductUnitProperty.objects.get(
                    product_unit=product_unit,
                    property=self
                ).property_value
                values_dict[value] = product_unit.id
            except ProductUnitProperty.DoesNotExist:
                pass

        return values_dict

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class ProductUnitProperty(models.Model):
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    property_value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.property}: {self.property_value} у товара {self.product_unit.product}'

    class Meta:
        verbose_name = "Хар-ка товара"
        verbose_name_plural = "Хар-ки товара"


class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_hidden = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Отзыв пользователя {self.profile} на товар {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
