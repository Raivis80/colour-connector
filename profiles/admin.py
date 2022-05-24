from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import FriendsList, Post, UserProfile, Color, Message, Image


# Register your models here.

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    fields = ('user', 'fav_color', 'slug')


@admin.register(FriendsList)
class FriendsListAdmin(admin.ModelAdmin):
    model = FriendsList
    list_display = ('user', 'friend', 'is_requested', 'is_accepted')


@admin.register(Color)
class ColorInline(admin.ModelAdmin):
    model = Color
    

@admin.register(Image)
class ImageInline(admin.ModelAdmin):
    model = Image


@admin.register(Message)
class MessageInline(admin.ModelAdmin):
    model = Message


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('sender', 'receiver', 'message', 'color', 'image')

    
class UserAdmin(BaseUserAdmin):
        inlines = (UserProfileAdmin,)
        
        
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)


