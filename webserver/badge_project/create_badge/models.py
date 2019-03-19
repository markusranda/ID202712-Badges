from django.db import models

# Create your models here.


class BadgeCreation(models.Model):
    image = models.ImageField(upload_to='event_badge', blank=True)


