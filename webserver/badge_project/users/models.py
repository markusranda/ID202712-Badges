from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    badge = models.ManyToManyField('badges.Badges', blank=True)
    about_me = models.CharField(max_length=255)
    email = models.CharField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True, max_length=6, blank=False)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})
