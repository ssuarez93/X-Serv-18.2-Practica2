from django.db import models

# Create your models here.

class Urls(models.Model):
    url_corta = models.CharField(max_length=32)
    url_larga = models.CharField(max_length=64)
