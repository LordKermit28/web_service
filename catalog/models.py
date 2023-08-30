
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    describing = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    date_create = models.DateField(null=True, blank=True)
    date_last_change = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    number = models.IntegerField(verbose_name='number')
    version_name = models.CharField(max_length=150, verbose_name='name')
    status = models.BooleanField(default=True, verbose_name='status')

    def __str__(self):
        return f"{self.version_name}"

    class Meta:
        verbose_name = 'version'
        verbose_name_plural = 'versions'


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True)
    content = models.TextField(verbose_name='content')
    preview = models.ImageField(null=True, blank=True)
    created_date = models.DateField(default=timezone.now)
    published_status = models.BooleanField(default=True, verbose_name='status')
    views_count = models.IntegerField(default=0, verbose_name='views')

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'




