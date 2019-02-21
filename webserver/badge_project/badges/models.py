from django.db import models


class Badges(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    image = models.ImageField('/images/badges/%Y/%m/%d/')
    user = models.ManyToManyField('users.CustomUser', blank=True)
    event = models.ManyToManyField('events.Events', blank=True)

