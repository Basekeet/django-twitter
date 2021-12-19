from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Profile model
    :user: reference to Django User model
    :bio: Profile description
    :friends: Profile friends
    :subs: Profile subs
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)
    subs = models.ManyToManyField("Profile", blank=True, related_name="%(class)s_subs")

    def __str__(self):
        """
        Prettify Profile printing
        """
        return 'Profile for user {}'.format(self.user.username)


class Post(models.Model):
    """
    Post model
    :author: reference to Post author
    :text: Post text
    :date: time when the post was created
    """
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.IntegerField(blank=True, default=0)
