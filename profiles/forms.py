from django import forms
from .models import FriendsList

# create a form class add friend
class AddFriendForm(forms.ModelForm):
    class Meta:
        model = FriendsList
        fields = ['friend']
