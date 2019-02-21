from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    badge = models.ManyToManyField('badges.Badges', blank=True)

    def __str__(self):
        return self.email
