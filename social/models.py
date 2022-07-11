from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)



class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=30, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        print("Stuck here?")
        UserProfile.objects.create(user=instance)
        print("Not stuck here")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()