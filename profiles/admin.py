from django.contrib import admin
from .models import FriendsList, Post


# Register your models here.
class FriendsListAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'is_requested', 'is_accepted')


class PostListAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'color', 'image')


admin.site.register(FriendsList, FriendsListAdmin)
admin.site.register(Post, PostListAdmin)
