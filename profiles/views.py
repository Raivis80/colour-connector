from ast import Return
from distutils.command.clean import clean
from operator import ge
from django.shortcuts import render, redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import *
from .forms import SendMessage
from django.db.models import Q

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
    user = get_object_or_404(UserProfile, user=request.user)

    friend = None
    if request.method == 'POST':
        if 'search' in request.POST:
            term = request.POST['search']
            # Check if the term is is not current user
            if term == request.user.username:
                message = 'You cannot add yourself as a friend'
                messages.warning(request, message)
                return redirect('profile')
            try:
                # search for single user with username excluding the current user
                friend = UserProfile.objects.get(user__username=term)
                message = 'Found user ' + friend.user.username
                messages.success(request, message)
            except ObjectDoesNotExist:
                message = 'User not found'
                messages.error(request, message)
                return redirect('profile')
        elif 'color' in request.POST:
            # Create change user fav color
            # ger color from form data and save it to the database
            try:
                color = request.POST['color']
                color_instance = Color.objects.get(color=color)
                user.fav_color = color_instance
                user.save()
                message = 'Color changed successfully to:' + color
                messages.success(request, message)
                return redirect('profile')
            except ObjectDoesNotExist:
                message = 'Color not found'
                messages.error(request, message)
                return redirect('profile')
        else:
            # create mood change request and save it to the user profile
            try:
                mood = request.POST['mood']
                mood_instance = Mood.objects.get(mood=mood)
                user.mood = mood_instance
                user.save()
                message = 'Mood changed successfully'
                messages.success(request, message)
                return redirect('profile')
            except ObjectDoesNotExist:
                message = 'Mood not found'
                messages.error(request, message)
                return redirect('profile')

    # get friend requests for the current user
    def get_requests_received(user):
        requests_received = FriendRequest.objects.filter(friend=user, is_accepted=False)
        if requests_received:
            return reversed((requests_received))
        return requests_received

    # get friend list for the current user and friends of the current user
    def get_all_friend_list(user):
        friend_list = FriendRequest.objects.filter(
            Q(user=user, is_accepted=True) | Q(friend=user, is_accepted=True))
        # exclude the current user from the friend list
        return friend_list
    
    # get friend requests sent by the current user
    def get_requests_sent(user):
        requests_sent = FriendRequest.objects.filter(
            user=user, is_requested=True, is_accepted=False)
        return requests_sent 
    
    # create search form for all users in the database
    # exclude the current user
    def get_search_form(user):
        form = User.objects.exclude(username=user).values_list('username', flat=True)
        return form

    def get_messages_received(user):
        messages_received = Post.objects.filter(receiver=user)
        return reversed(messages_received)
    
    context = {
        'mood': user.mood,
        'moods': Mood.objects.all(),
        'action': 'profile',
        'fav_color': user.fav_color,
        'colors': Color.objects.all(),
        'messages_received': get_messages_received(user),
        'friend': friend,
        'friend_list': get_all_friend_list(user),
        'requests_received': get_requests_received(user),
        'requests_sent': get_requests_sent(user),
        'form': get_search_form(user)
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def user_profile(request, slug):
    """
    Display the friend's profile views.
    POST method is used to send a message to the friend
  
    """
    # find the user with the search query
    friend = get_object_or_404(UserProfile, slug=slug)
    friend_mood = str(friend.mood)
    # Get color list
    colors = Color.objects.all()
    form = SendMessage()
    # create user views
    context = {
        'colors': colors,
        'friend': friend,
        'form': form
    }
    return render(request, 'profiles/friend-detail.html', context)
            

@require_POST
def add_friend(request):
    """
    Add a friend to the current user's friend list
    POST method required get user's username from the form
    Find the user with the username and add
    it to the current user's friend list
    """
    form = AddFriendForm(request.POST)
    if form.is_valid():
        # get the current user
        user = get_object_or_404(UserProfile, user=request.user)
        # get the friend
        friend = form.cleaned_data['friend']
        friend = get_object_or_404(UserProfile, user__username=friend)
        # Check if the user is already a friend
        if FriendRequest.objects.filter(user=user, friend=friend, is_requested=True).exists():
            message = 'Friend request pending or you are already friends'
            messages.error(request, message)
            return redirect('profile')
        elif FriendRequest.objects.filter(user=friend, friend=user, is_requested=True).exists():
            message = 'Friend request already received from this person Please accept the friend request'
            messages.error(request, message)
            return redirect('profile')     
        # create a new friend request
        try:
            # create user's friend request object and save it
            friend_request = FriendRequest(user=user, friend=friend, is_requested=True)
            friend_request.save()
            message = 'Friend request sent to ' + friend.user.username
            messages.success(request, message)
            return redirect('profile')
        except ObjectDoesNotExist:
            message = 'Something went wrong while adding friend'
            messages.error(request, message)
            return redirect('profile')
    else:
        message = 'Invalid form data please try again'
        messages.error(request, message)
        return redirect('profile')


@require_POST
def accept_friend(request):
    """
    Accept a friend request function
    requires a POST to get request id  from the form
    find user in database based on the friend's username
    """
    request_id = request.POST['request_id']
    user = get_object_or_404(UserProfile, user=request.user)
    try:
        #accept friend request and save it
        accept_request = FriendRequest.objects.get(id=request_id)
        accept_request.is_accepted = True
        accept_request.save()
        message = 'You are now friends with ' + accept_request.friend.user.username
        messages.success(request, message)
        return redirect('profile')
    
    except ObjectDoesNotExist:
        message = 'Could not find friend request in the database'
        messages.error(request, message)
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
        user = get_object_or_404(UserProfile, user=request.user)
        # delete the friend from the current user's friend list
        delete_friend = FriendRequest.objects.get(user=user, friend=friend.id)
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
    form = SendMessage(request.POST)

    try:
        # get the current user
        sender = get_object_or_404(UserProfile, user=request.user)
        receiver = UserProfile.objects.get(user__id=request.POST['receiver'])
        message = request.POST['message']
        color = request.POST['color']
        color_instance = Color.objects.get(color=color)
        message_instance = Message(id=message)
        get_send_message = Post(
            sender=sender, receiver=receiver, message=message_instance, color=color_instance)
        get_send_message.save()
        
        message = 'Message sent successfully to ' + receiver.user.username
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        message = "There was an issue sending message please try again later"
        return redirect(request.META.get('HTTP_REFERER'))
        return redirect('profile')


@login_required
def post_detail(request, slug):
    """
    Display the Post detail page
  
    """
    # find the user with the search query
    post = get_object_or_404(Post, slug=slug)
    # create user views
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
