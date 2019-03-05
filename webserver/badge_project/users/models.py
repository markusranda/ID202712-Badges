from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    badge = models.ManyToManyField('badges.Badges', blank=True)
    id = models.IntegerField(unique=True, primary_key=True)
    last_login = models.DateField(max_length=6)
    email = models.CharField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True, max_length=6, blank=False)

    def __str__(self):
        return self.email
