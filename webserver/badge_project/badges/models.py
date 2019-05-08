from django.db import models


class Badges(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    image = models.ForeignKey('Images', on_delete=models.CASCADE,)


class Images(models.Model):
    name = models.CharField(max_length=50)
    url = models.ImageField('/badges/', blank=True)

    def __str__(self):
        return str(self.url)