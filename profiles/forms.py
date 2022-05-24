from django import forms
from .models import FriendsList, Post


# create a form class add friend
class AddFriendForm(forms.ModelForm):
    class Meta:
        model = FriendsList
        fields = ['friend']


class SendMessage(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['sender', 'receiver', 'message', 'color', 'image']