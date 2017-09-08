from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from eforce_api.models import UserProfile


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_userprofile(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
