from cProfile import label
from django import forms
from .models import FriendRequest, Post


# create a form class add friend
class AddFriendForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['friend']


class SendMessage(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['sender', 'receiver', 'message', 'color', 'image']
        
    # add placeholder to the form
    def __init__(self, *args, **kwargs):
        super(SendMessage, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
            # set default option django forms
            self.fields[field].empty_label = 'Please select ' + self.fields[field].label
            
        
    