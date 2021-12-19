from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)
    subs = models.ManyToManyField("Profile", blank=True, related_name="%(class)s_subs")

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Post(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.IntegerField(blank=True, default=0)
