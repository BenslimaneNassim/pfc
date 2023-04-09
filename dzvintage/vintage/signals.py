# from allauth.socialaccount.models import SocialAccount
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Profile
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
import requests

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        if instance.socialaccount_set.filter(provider='Google').exists():
            socialaccount = instance.socialaccount_set.get(provider='Google')
            url = socialaccount.extra_data['picture']
            response = requests.get(url)
            if response.status_code == 200:
                profile.picture.save(f'{instance.username}.jpg', response.content, save=True)
