from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    event_badge = models.ManyToManyField('events.EventBadges', through="UserBadges", related_name='event_badges', blank=True)
    about_me = models.CharField(max_length=255)
    email = models.CharField(max_length=254)
    events = models.ManyToManyField('events.Events', through='Attendees', related_name='attendingEvents')
    badge_request = models.ManyToManyField('badges.Badges', through='events.BadgeRequests', related_name='badge_request')
    color_value = models.CharField(max_length=7, default='#d76565')

    def event_badge_count_of(self, event_id):
        return self.event_badge.filter(event_id=event_id).count()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})


class Attendees(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='attending')
    event = models.ForeignKey('events.Events', on_delete=models.CASCADE, related_name='attending')


class UserBadges(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='userbadge')
    is_showcase = models.BooleanField(default=0)
    date_earned = models.DateTimeField(auto_now_add=True, blank=False)
    event_badge = models.ForeignKey('events.EventBadges', on_delete=models.CASCADE, related_name='user_badges')
