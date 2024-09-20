from django.db import models

# Create your models here.
class Link(models.Model):
    link = models.URLField("youtube link", unique=True)