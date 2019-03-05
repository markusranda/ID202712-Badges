from django.db import models


class Badges(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    image = models.ImageField('/badges/', blank=True)
    user = models.ManyToManyField('users.CustomUser', blank=True)
    event = models.ManyToManyField('events.Events', blank=True)
    is_showcase_of = models.ForeignKey(
        'users.CustomUser', related_name='is_showcase_of', blank=True, null=True, on_delete=models.CASCADE)
