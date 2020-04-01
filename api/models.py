from django.db import models
from api.fields import JSONField

# Create your models here.
class Category(models.Model):
    object = models.Manager()
    title = models.TextField()
    description = models.TextField()

class Product(models.Model):
    object = models.Manager()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.TextField()
    description = models.TextField()
    filename = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Sale(models.Model):
    object = models.Manager()
    name = models.TextField()
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items = JSONField(default=dict)
    payment_intent = JSONField(default=dict)