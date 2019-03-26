from django.db import models
from django.utils.crypto import get_random_string


def random():
    rand = get_random_string(5, '0123456789')
    return rand


class Events(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=1)
    pin = models.IntegerField(unique=True, default=random)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='createdBy')

    events = models.ManyToManyField('users.CustomUser', through='users.Attendees', related_name='attendingEvents')


class BadgeRequests(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='request')
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='request')
    badge = models.ForeignKey('badges.Badges', on_delete=models.CASCADE, related_name='request')


class EventBadges(models.Model):
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='eventbadge')
    badge = models.ForeignKey('badges.Badges', on_delete=models.CASCADE, related_name='eventbadge')
