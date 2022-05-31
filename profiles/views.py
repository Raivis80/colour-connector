from django.shortcuts import render, redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
import json

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

    # get friend requests for the current user
    def get_requests_received(user):
        requests_received = FriendRequest.objects.filter(friend=user, is_accepted=False)
        if requests_received:
            return requests_received
        return requests_received

    # get friend list for the current user and friends of the current user
    def get_all_friend_list(user):
        friend_list = FriendRequest.objects.filter(
            Q(user=user, is_accepted=True) | Q(friend=user, is_accepted=True))
        friend_list = friend_list.order_by('creation_time')
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
        messages_received = Post.objects.filter(receiver=user).order_by('creation_time')
        return reversed(messages_received)
    
    def get_notifications(user):
        notifications = messages_received.union(get_requests_received(user))
    
    if request.htmx:
        context = {
            'messages_received': get_messages_received(user),
            'requests_received': get_requests_received(user),
        }
        return render (request, 'includes/received-messages.html', context)
    else:
        messages_received = get_messages_received(user)

    context = {
        'mood': user.mood,
        'moods': Mood.objects.all(),
        'action': 'profile',
        'fav_color': user.fav_color,
        'colors': Color.objects.all(),
        'messages_received': messages_received,
        'friend': friend,
        'friend_list': get_all_friend_list(user),
        'requests_received': get_requests_received(user),
        'requests_sent': get_requests_sent(user),
        'form': get_search_form(user)
    }
    return render(request, 'profiles/profile.html', context)


@require_POST
def search_user(request):
    """
    Check if the username is available
    """
    user = get_object_or_404(UserProfile, user=request.user)
    username = request.POST['search']
    if UserProfile.objects.filter(user__username=username).exists():
        friend = UserProfile.objects.get(user__username=username)
        is_friend = FriendRequest.objects.filter(
            Q(user=user, friend=friend) | Q(user=friend, friend=user))
        is_myself = user.user.username == friend.user.username
        if is_friend:
            resp_message = "<div class='text-info'>You are already friends with this user</div>"
            return HttpResponse(resp_message)
        elif is_myself:
            resp_message = "<div class='text-info'>You can't add yourself as a friend</div>"
            return HttpResponse(resp_message)
        context = {
            'show': 'show',
            'friend': friend,
        }
        return render(request, 'includes/toasts/send-request.html', context)
    else:
        resp_message = "<div class='text-danger'>No user with this username found</div>"
        return HttpResponse(resp_message)


@require_POST
def change_mood(request):
    """
    Change the mood of the user
    """
    user = get_object_or_404(UserProfile, user=request.user)
    mood = request.POST['mood']
    mood_instance = Mood.objects.get(mood=mood)
    user.mood = mood_instance
    user.save()
    context = {
        'mood': mood,
        'active': 'active',
    }
    return render(request, 'includes/mood-button.html', context)


@require_POST
def change_color(request):
    """
    Change the fav color of the user
    """
    user = get_object_or_404(UserProfile, user=request.user)
    color = request.POST['color']
    color_instance = Color.objects.get(color=color)
    user.fav_color = color_instance
    user.save()
    context = {
        'fav_color': color,
        'active': 'active',
    }
    return render(request, 'includes/color-button.html', context)


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
            # get friend list for the current user and friends of the current user
        def get_all_friend_list(user):
            friend_list = FriendRequest.objects.filter(
                Q(user=user, is_accepted=True) | Q(friend=user, is_accepted=True))
            friend_list = friend_list.order_by('creation_time')
            # exclude the current user from the friend list
            return friend_list
        message = 'You are now friends with ' + accept_request.friend.user.username
        messages.success(request, message)
        context = {
            'friend_list': get_all_friend_list(user),
        }
        return render(request, 'includes/friend-list.html', context)
    
    except ObjectDoesNotExist:
        message = 'Could not find friend request in the database'
        messages.error(request, message)
        return redirect('profile')
    

@require_POST
def reject_friend(request):
    """
    Reject a friend request function
    requires a POST to get request id  from the form
    find user in database based on the friend's username
    """
    request_id = request.POST['request_id']
    user = get_object_or_404(UserProfile, user=request.user)
    try:
        #reject friend request and save it
        reject_request = FriendRequest.objects.get(id=request_id)
        reject_request.delete()
        message = 'You have rejected ' + reject_request.friend.user.username + '\'s friend request'
        messages.success(request, message)
        return redirect('profile')
    
    except ObjectDoesNotExist:
        message = 'Could not find friend request in the database'
        messages.error(request, message)
        return redirect('profile')


@require_POST
def unfriend(request, friend_id):
    """
    Delete a friend from the current user's friend list
    Send a delete request via htmx delete method
    """
    try:     
        friend = get_object_or_404(UserProfile, id=friend_id)
        # get the current user
        user = get_object_or_404(UserProfile, user=request.user)
        # delete the friend from the current user's friend list
        delete_friend = FriendRequest.objects.filter(Q(user=user, friend=friend) | Q(user=friend, friend=user))
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
    Get the message from the form and
    Save the message to the database 
    and redirect to the friend's profile
    """
    form = SendMessage(request.POST)
    # Form validation check if the form is valid
    if 'message' in request.POST and request.POST['message'] != '':
        message = request.POST['message']
        message_instance = Message(id=message)
    else:
        message = 'Message is empty, please select a message'
        messages.error(request, message)
        return redirect(request.META.get('HTTP_REFERER'))
    if 'color' in request.POST and request.POST['color'] != '':
        color = request.POST['color']
        color_instance = Color.objects.get(color=color)
    else:
        message = 'Color is empty, please select a color'
        messages.error(request, message)
        return redirect(request.META.get('HTTP_REFERER'))
    # If the form is valid try to save the message
    try:
        # get the current user
        sender = get_object_or_404(UserProfile, user=request.user)
        receiver = UserProfile.objects.get(user__id=request.POST['receiver'])
        
        get_send_message = Post(
            sender=sender, receiver=receiver, message=message_instance, color=color_instance)
        get_send_message.save()
        
        message = 'Message sent successfully to ' + receiver.user.username
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        message = "There was an issue sending message please try again later"
        return redirect(request.META.get('HTTP_REFERER'))


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
    return render(request, 'posts/post-detail.html', context)
