from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=25)
    e_mail = models.EmailField(max_length=100)
    password = models.CharField(max_length=25)


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
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = [
            ("user_id", "event_id"),
        ]


class EventBadges(models.Model):
    badge_id = models.ForeignKey(Badges, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = [
            ("badge_id", "event_id"),
        ]


class UserBadges(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    badge_id = models.ForeignKey(Badges, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = [
            ("user_id", "badge_id"),
        ]
