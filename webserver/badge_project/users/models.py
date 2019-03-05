from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    badge = models.ManyToManyField('badges.Badges', blank=True)
    showcase_badge = models.ManyToManyField('badges.Badges', blank=True, null=True, on_delete=models.CASCADE)
    about_me = models.CharField(max_length=255)
    email = models.CharField(max_length=254)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})
