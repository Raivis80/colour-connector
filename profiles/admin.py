from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *


# Register your models here.

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = False

@admin.register(FriendRequest)
class FriendsListAdmin(admin.ModelAdmin):
    model = FriendRequest


@admin.register(Color)
class ColorInline(admin.ModelAdmin):
    model = Color
    

@admin.register(Image)
class ImageInline(admin.ModelAdmin):
    model = Image
    
    
@admin.register(Mood)
class MoodInline(admin.ModelAdmin):
    model = Mood


@admin.register(Message)
class MessageInline(admin.ModelAdmin):
    model = Message


class PostAdmin(admin.ModelAdmin):
    model = Post


class UserAdmin(BaseUserAdmin):
        inlines = (UserProfileAdmin,)
        
        
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)


