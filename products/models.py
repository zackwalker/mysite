from django.db import models

class Product(models.Model):
    title         = models.CharField(max_length=120)
    description   = models.TextField(blank=True, null=True) #blank is how field is rendered, null is the database
    price         = models.DecimalField(decimal_places=2, max_digits=10000)
    summary       = models.TextField()
    featured      = models.BooleanField(default=False)
