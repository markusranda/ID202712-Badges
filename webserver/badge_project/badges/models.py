from django.db import models


class Badges(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    image = models.ImageField('/badges/', blank=True)


class Images(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255)