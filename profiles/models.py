from operator import pos
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import Q
import uuid


# Crate a color model
class Color(models.Model):
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.color)
    

# Create your models here.
class UserProfile(models.Model):
    """
    The User Profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fav_color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE, null=True)
    
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    slug = models.SlugField(unique=True)
    
    def get_absolute_url(self):
        return reverse('user_profile', args=[self.slug])
         
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)


# Friend list modal
class FriendRequest(models.Model):
    """
    The Friend List
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='request_user')
    friend = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friend')
    is_requested = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.user.user.username)

    
# Crete a image link model
class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image
    

# create a Message model
class Message(models.Model):
    message = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return str(self.message)
    

class Mood(models.Model):
    mood = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return str(self.mood)
    

# Messages
class Post(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE , null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='receiver', blank=True, null=True)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, blank=True, null=True)
    
    seen = models.BooleanField(default=False)
    
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)	
    
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.message)


#Create post_save receiver to create user profile for every new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
    else:
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)

          
#Create post delete uf unfriend delete posts 
@receiver(post_delete, sender=FriendRequest)
def delete_post(sender, instance, **kwargs):
    try:
        posts_to_delete = Post.objects.filter(Q(sender=instance.user) | Q(receiver=instance.user) | Q(sender=instance.friend) | Q(receiver=instance.friend))
        
        for post in posts_to_delete:
            post.delete()
    except ObjectDoesNotExist:
        pass
