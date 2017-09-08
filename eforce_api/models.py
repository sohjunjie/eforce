from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(max_length=500, null=True)
    avatar = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username
