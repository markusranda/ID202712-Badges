from django.db import models


class Events(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    pin = models.IntegerField(unique=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)


class BadgeRequests(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='request')
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='request')
    badge = models.ForeignKey('badges.Badges', on_delete=models.CASCADE, related_name='request')
