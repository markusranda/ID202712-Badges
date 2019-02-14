from django.db import models


class Events(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    pin = models.IntegerField(unique=True)


class Badges(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    image = models.ImageField()


class Attendees(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = [
            ("user", "event"),
        ]


class EventBadges(models.Model):
    badge = models.ForeignKey(Badges, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = [
            ("badge", "event"),
        ]


class UserBadges(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    badge = models.ForeignKey(Badges, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = [
            ("user", "badge"),
        ]
