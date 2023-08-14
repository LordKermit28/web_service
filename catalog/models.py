from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    describing = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    describing =models.CharField(max_length=150)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    date_create = models.DateField(null=True, blank=True)
    date_last_change = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


