from django.db import models
from django.utils.crypto import get_random_string


# Shady
def random():
    rand = get_random_string(5, '0123456789')
    return rand

class Events(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=1)
    pin = models.IntegerField(unique=True, default=random())
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='createdBy')
    attendees = models.ManyToManyField('users.CustomUser', through='users.Attendees', related_name='attendingEvents')
    badge = models.ManyToManyField('badges.Badges', through='EventBadges', related_name='eventBadges')


class BadgeRequests(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='request')
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='request')
    badge = models.ForeignKey('badges.Badges', on_delete=models.CASCADE, related_name='request')

    def __str__(self):
        return str(self.user) + str(self.event) + str(self.badge)


class EventBadges(models.Model):
    badge = models.ForeignKey('badges.Badges', on_delete=models.CASCADE, related_name='userbadge')
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='event')
