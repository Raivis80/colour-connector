from django.contrib import admin
from .models import FriendsList


# Register your models here.
class FriendsListAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'is_requested', 'is_accepted')

admin.site.register(FriendsList, FriendsListAdmin)
