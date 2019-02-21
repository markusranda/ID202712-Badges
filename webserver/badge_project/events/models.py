from django.db import models


class Events(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    pin = models.IntegerField(unique=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    user = models.ManyToManyField('users.CustomUser', related_name='attendant', blank=True)
