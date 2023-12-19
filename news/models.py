from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from transliterate import translit

from users.models import User


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=150, verbose_name='Название статьи')
    text = models.TextField(verbose_name='Текст статьи')
    date_published = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True, editable=False, unique=True)

    def __str__(self):
        return f'{self.title} (/{self.slug})'

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
