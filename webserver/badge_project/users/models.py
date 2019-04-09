from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    badge = models.ManyToManyField('badges.Badges', through="UserBadges", related_name='userbadges', blank=True)
    about_me = models.CharField(max_length=255)
    email = models.CharField(max_length=254)
    events = models.ManyToManyField('events.Events', through='Attendees', related_name='attendingEvents')
    badge_request = models.ManyToManyField('badges.Badges', through='events.BadgeRequests', related_name='badge_request')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})


class Attendees(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='attending')
    event = models.ForeignKey('events.Events', on_delete=models.CASCADE, related_name='attending')


class UserBadges(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='userbadge')
    badge = models.ForeignKey('badges.Badges', on_delete=models.CASCADE, related_name='userbadge')
    event = models.ForeignKey('events.Events', on_delete=models.CASCADE, related_name='userbadge')
    is_showcase = models.BooleanField()
