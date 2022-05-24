from django.shortcuts import render, redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import UserProfile, Post
from .forms import SendMessage
from django.db.models import Q

from .models import FriendsList
from .forms import AddFriendForm

# Create your views here.

@login_required
def profile(request):
    """
    Display the user's profile.
    Get all friends of the logged in user's friends
    Get friend requests of the logged in user
    Get Requests sent by the logged in user
    POST method is used to search for friends
    Return form to add friend 
    Pass all the above data to profile.html and render profile template
    """
    # profile = get_object_or_404(UserProfile, user=request.user)

    # find the user with the search query
    friend = None
    if request.method == 'POST':
        term = request.POST['search']

        try:
            # search for single user with username excluding the current user
            friend = User.objects.exclude(
                username=request.user.username).get(username=term)
            
            message = 'Found user ' + friend.username
            messages.success(request, message)

        except ObjectDoesNotExist:
            message = 'User not found'
            messages.error(request, message)
            return redirect('profile')

    # get friend list for the current user and friends of the current user
    def get_all_friend_list(user):
        friend_list = FriendsList.objects.filter(Q(user=user, is_accepted=True) | Q(friend=user, is_accepted=True))
        return friend_list
    
    # get friend requests for the current user
    def get_requests_received(user):
        requests_received = FriendsList.objects.filter(friend=user, is_requested=True, is_accepted=False)
        return requests_received
    
    # get friend requests sent by the current user
    def get_requests_sent(user):
        requests_sent = FriendsList.objects.filter(user=user, is_requested=True, is_accepted=False)
        return requests_sent 
    
    # create search form for all users in the database
    # exclude the current user
    def get_search_form(user):
        form = User.objects.exclude(username=user.username).values_list('username', flat=True)
        return form

    def get_messages_received(user):
        messages_received = Post.objects.filter(receiver=user)
        return messages_received
    
    
    context = {
        'messages_received': get_messages_received(request.user),
        'friend': friend,
        'friend_list': get_all_friend_list(request.user),
        'requests_received': get_requests_received(request.user),
        'requests_sent': get_requests_sent(request.user),
        'form': get_search_form(request.user)
    }

    return render(request, 'profiles/profile.html', context)


@require_POST
def add_friend(request):
    """
    Add a friend to the current user's friend list
    POST method required get user's username from the form
    Find the user with the username and add
    it to the current user's friend list
    """
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            # get the friend
            friend = form.cleaned_data['friend']
            # get the current user
            user = request.user
            # Check if the user is already a friend
            if FriendsList.objects.filter(user=user, friend=friend, is_accepted=True).exists():
                message = 'User is already a friend'
                messages.error(request, message)
                return redirect('profile')
            elif FriendsList.objects.filter(user=friend, friend=user, is_accepted=True).exists():
                message = 'User is already a friend'
                messages.error(request, message)
                return redirect('profile')
            # create a new friend request
            try:
                # create user's friend request object and save it
                friend_request = FriendsList(user=user, friend=friend, is_requested=True)
                friend_request.save()
                message = 'Friend request sent to ' + friend.username
                messages.success(request, message)
                return redirect('profile')
            except ObjectDoesNotExist:
                message = 'Something went wrong while adding friend'
                messages.error(request, message)
                return redirect('profile')
        else:
            message = 'Invalid form'
            messages.error(request, message)
            return redirect('profile')


@require_POST
def accept_friend(request):
    """
    Accept a friend request function
    requires a POST to get username from the form
    find user in database based on the friend's username
    """
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            # get the username of the friend from the form
            friend = form.cleaned_data['friend']
            user = request.user
            # Check if the user is already a friend
            if FriendsList.objects.filter(user=user, friend=friend, is_accepted=True).exists():
                message = 'User is already a friend'
                messages.error(request, message)
                return redirect('profile')
            elif FriendsList.objects.filter(user=friend, friend=user, is_accepted=True).exists():
                message = 'User is already a friend'
                messages.error(request, message)
                return redirect('profile')
            try:
                #accept friend request and save it
                accept_request = FriendsList.objects.get(user=friend, friend=user, is_requested=True, is_accepted=False)
                accept_request.is_accepted = True
                accept_request.save()
                message = 'You are now friends with ' + friend.username
                messages.success(request, message)
                return redirect('profile')
            
            except ObjectDoesNotExist:
                message = 'Could not find friend request in the database'
                messages.error(request, message)
                return redirect('profile')
        else:
            error = 'Check spelling of username and try again' 
            messages.error(request, error)
            return redirect('profile')


@require_POST
def delete_friend(request):
    """
    Delete a friend from the current user's friend list
    POST is required to get the username from the form
    """
    try:     
        friend = User.objects.get(username=request.POST['friend'])
        # get the current user
        user = request.user
        # delete the friend from the current user's friend list
        delete_friend = FriendsList.objects.get(user=user, friend=friend.id)
        delete_friend.delete()
        message = 'Friend deleted'
        messages.success(request, message)
        return redirect('profile')
    except ObjectDoesNotExist:
        message = 'Could not find friend in the database'
        messages.error(request, message)
        return redirect('profile')


@require_POST
def send_message(request):
    """
    Send message to user requires POST
    """
    try:
        # get the current user
        sender = request.user
        receiver = User.objects.get(username=request.POST['receiver'])
        message = request.POST['message']
        color = request.POST['color']
        # delete the friend from the current user's friend list
        get_send_message = Post(sender=sender,
                                receiver=receiver,
                                message=message,
                                color=color)
        get_send_message.save()
        message = 'Messsage sent succesfully to ' + receiver.username
        messages.success(request, message)
        return redirect('profile')
    except ObjectDoesNotExist:
        message = "There was an issue sending message please try again later"
        messages.error(request, message)
        return redirect('profile')
