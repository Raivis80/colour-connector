from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserProfile(models.Model):
    """
    The User Profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Friend list modal
class FriendsList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    is_requested = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + ' ' + self.friend.username
