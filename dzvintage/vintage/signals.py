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
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile, Article_Like, Post, Abonnement, Transaction

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

@receiver(post_save, sender=Article_Like)
def increment_likes(sender, instance, created, **kwargs):
    if created:
        instance.post.nb_likes += 1
        instance.post.save()

@receiver(post_delete, sender=Article_Like)
def decrement_likes(sender, instance, **kwargs):
    instance.post.nb_likes -= 1
    instance.post.save()

@receiver(post_save, sender=Abonnement)
def update_followers_and_following_on_abonnement_create(sender, instance, created, **kwargs):
    if created:
        # A new Abonnement instance is created
        # Increment the nb_followers count of the followed user's profile
        instance.followed.profile.nb_followers += 1
        instance.followed.profile.save()

        # Increment the nb_following count of the follower user's profile
        instance.follower.profile.nb_following += 1
        instance.follower.profile.save()

@receiver(post_delete, sender=Abonnement)
def update_followers_and_following_on_abonnement_delete(sender, instance, **kwargs):
    # An Abonnement instance is deleted
    # Decrement the nb_followers count of the followed user's profile
    instance.followed.profile.nb_followers -= 1
    instance.followed.profile.save()

    # Decrement the nb_following count of the follower user's profile
    instance.follower.profile.nb_following -= 1
    instance.follower.profile.save()

@receiver(post_save, sender=Transaction)
def update_transactions_on_transaction_create(sender, instance, created, **kwargs):
    if created:
        chat = instance.post.chats.create(sender=instance.post.seller, receiver=instance.user, message="Transaction effectuée")
        
