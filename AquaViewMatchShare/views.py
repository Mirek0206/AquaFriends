from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from AquaViewMatchShare.models import User, Matches
from .models import Message
from AquaMaker.models import Aquarium
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime


# Create your views here.

@login_required(login_url='login')
def lobby(request):
    """
    Lobby view that displays chat conversations to a logged in user.
    It fetches a list of friends that the user has matched with,
    fetches the most recent message for each friend, and sorts the friends
    list by the timestamp of the last message.
    For the friend with the most recent message, it fetches the last 10 messages.

    :param request: The request object.
    :type request: HttpRequest

    :return: Rendered HTML page.
    :rtype: HttpResponse
    """
    AMOUNT_OF_FRIENDS = 10  # TODO: maybe change ?
    page = 'chat'
    matches = Matches.objects.filter(
        Q(first_user=request.user, first_status=True, second_status=True) |
        Q(second_user=request.user, second_status=True, first_status=True)
    )

    friends = list(User.objects.filter(
        Q(id__in=matches.values_list('first_user', flat=True))
        | Q(id__in=matches.values_list('second_user', flat=True))
    ).exclude(id=request.user.id))

    # find one message for every friend
    for friend in friends:
        message = Message.objects.filter(
            Q(sender_id=request.user, recipient_id=friend) |
            Q(sender_id=friend, recipient_id=request.user)
        ).order_by('-send_timestamp').first()
        friend.last_message = message

    # sort friends based on the last message timestamp
    friends = sorted(
        friends,
        key=lambda f: getattr(f.last_message, 'send_timestamp', timezone.make_aware(datetime.min)),
        reverse=True
    )

    # get 10 recent messages from friend with most recent message
    recent_friend = friends[0] if friends else None  # get the first friend
    if recent_friend:
        last_10_messages = Message.objects.filter(
            Q(sender_id=request.user, recipient_id=recent_friend) |
            Q(sender_id=recent_friend, recipient_id=request.user)
        ).order_by('-send_timestamp')[:10]

        recent_friend.messages = reversed(last_10_messages)

    context = {
        'friends': friends[:AMOUNT_OF_FRIENDS],
        'page': page
    }
    return render(request, 'lobby.html', context=context)

@login_required(login_url='login')
def findBestMatch(request):
    user = request.user
    user_aquariums = Aquarium.objects.filter(user=user)
    matched_user_ids = [user.id]

    scores = {}
    for other_user in User.objects.exclude(id__in=matched_user_ids):
        other_user_aquariums = Aquarium.objects.filter(user=other_user)
        score = 0

        for user_aquarium in user_aquariums:
            for other_aquarium in other_user_aquariums:
                score += (user_aquarium.light_id == other_aquarium.light_id) + \
                         (user_aquarium.pump_id == other_aquarium.pump_id) + \
                         (user_aquarium.heater_id == other_aquarium.heater_id) + \
                         (user_aquarium.filters.filter(id__in=other_aquarium.filters.all()).count()) + \
                         (user_aquarium.decorators.filter(id__in=other_aquarium.decorators.all()).count())

        scores[other_user.id] = score

    if scores:
        best_match_user_id = max(scores, key=scores.get)
        best_match_user = User.objects.get(id=best_match_user_id)

        context = {
            'best_match_user': best_match_user,
            'aquariums': Aquarium.objects.filter(user=best_match_user)
        }
    else:
        messages.error(request, 'Aktualnie nie ma więcej użytkowników, których moglibyśmy do Ciebie dopasować.')
        return redirect('account')

    return render(request, 'best_match.html', context)


@require_POST
@login_required(login_url='login')
def acceptMatch(request, user_id):
    """
    Accept a match by creating a new Match instance with the first_status set to True.

    Args:
        request (HttpRequest): The request instance.
        user_id (int): The ID of the user to be matched with.

    Returns:
        HttpResponseRedirect: Redirect to the 'find_best_match' view.
    """
    # Get the other user
    other_user = User.objects.get(id=user_id)

    # Create a new Match object with first_status=True
    match = Matches(first_user=request.user, second_user=other_user, first_status=True, second_status=None)
    match.save()

    return redirect('find_best_match')

@require_POST
@login_required(login_url='login')
def rejectMatch(request, user_id):
    """
    Reject a match by creating a new Match instance with the first_status set to False.

    Args:
        request (HttpRequest): The request instance.
        user_id (int): The ID of the user to be matched with.

    Returns:
        HttpResponseRedirect: Redirect to the 'find_best_match' view.
    """
    # Get the other user
    other_user = User.objects.get(id=user_id)

    # Create a new Match object with first_status=False
    match = Matches(first_user=request.user, second_user=other_user, first_status=False, second_status=False)
    match.save()

    return redirect('find_best_match')

@login_required(login_url='login')
def getOldestLike(request):
    user = request.user
    matches = Matches.objects.filter(second_user=user, first_status=True, second_status=None)

    if not matches:
        messages.error(request, 'Aktualnie nie masz żadnych polubień swojego profilu.')
        return redirect('account')

    oldest_match = matches.earliest('id')
    context = {
        'matched_user': oldest_match.first_user,
        'aquariums': Aquarium.objects.filter(user=oldest_match.first_user)
    }

    return render(request, 'oldest_like.html', context)

@require_POST
@login_required(login_url='login')
def acceptLike(request, user_id):
    """
    Accept a like by setting the second_status of the Match instance to True.

    Args:
        request (HttpRequest): The request instance.
        user_id (int): The ID of the user who liked the currently logged-in user.

    Returns:
        HttpResponseRedirect: Redirect to the 'get_oldest_like' view.

    Raises:
        Http404: The match instance does not exist.
    """
    # Pobierz innego użytkownika
    other_user = get_object_or_404(User, id=user_id)

    # Znajdź obiekt Matches, który spełnia określone kryteria
    match = get_object_or_404(Matches,
                              first_user=other_user,
                              second_user=request.user,
                              first_status=True,
                              second_status=None)

    # Zaktualizuj wartość second_status na True
    match.second_status = True
    match.save()

    return redirect('get_oldest_like')

@require_POST
@login_required(login_url='login')
def rejectLike(request, user_id):
    """
    Reject a like by setting the second_status of the Match instance to False.

    Args:
        request (HttpRequest): The request instance.
        user_id (int): The ID of the user who liked the currently logged-in user.

    Returns:
        HttpResponseRedirect: Redirect to the 'get_oldest_like' view.

    Raises:
        Http404: The match instance does not exist.
    """
    # Pobierz innego użytkownika
    other_user = get_object_or_404(User, id=user_id)

    # Znajdź obiekt Matches, który spełnia określone kryteria
    match = get_object_or_404(Matches,
                              first_user=other_user,
                              second_user=request.user,
                              first_status=True,
                              second_status=None)

    # Zaktualizuj wartość second_status na True
    match.second_status = False
    match.save()

    return redirect('get_oldest_like')
