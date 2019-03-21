from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    badge = models.ManyToManyField('badges.Badges', blank=True)
    showcase_badge = models.ManyToManyField('badges.Badges', related_name='is_showcase_badge', blank=True)
    about_me = models.CharField(max_length=255)
    email = models.CharField(max_length=254)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})


class Attendees(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='attending')
    event = models.ForeignKey('events.Events', on_delete=models.CASCADE, related_name='attending')
