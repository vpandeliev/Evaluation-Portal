import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import *
from models import *
from choices import *


def index(request):
    context = {
        'title': 'Boggle games',
        'new_games': Game.objects.filter(state=game_states.WAITING_FOR_PLAYERS),
        'active_games': Game.objects.filter(state=game_states.IN_PROGRESS),
    }
    return render_to_response('boggle/index.html', context)


@login_required
def create_new_game(request):
    '''
    Optional GET arguments are:
        play_for - number of rounds to play for, default 10
        return_to - URL to return to after the maximum # of rounds has been played
    '''
    
    play_for = request.GET.get('play_for', 10)
    return_to = request.GET.get('return_to', '/')
    query = request.GET.urlencode()
    game = Game.objects.create(round_max=play_for, game_over_url=return_to)
    return join_game(request, game.id, query)

#to change state of next game, need to get parameter for mode type...[LIAM]
@login_required
def start_round(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    # In case somebody else already started the game.
    if game.state == game_states.WAITING_FOR_PLAYERS:
        game.start_round(mode=boggle_modes.NORMAL)

    return HttpResponseRedirect(reverse('play-boggle-game', kwargs={'game_id': game.id}))


@login_required
def next_round(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.is_over:
        game.end_round()
        return HttpResponseRedirect(reverse('game-over', kwargs={'game_id': game.id}))
    # In case somebody else already started the next round
    if game.round.time_left() == 0:
        game.goto_next_round(mode=boggle_modes.NORMAL)
    return HttpResponseRedirect(reverse('play-boggle-game', kwargs={'game_id': game.id}))


@login_required
def leave_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    try:
        player = game.player_set.active().get(user=request.user)
        player.leave_game()
    except Player.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('boggle-index'))


@login_required
def join_game(request, game_id, query_string):
    game = get_object_or_404(Game, pk=game_id)
    
    if game.state == game_states.COMPLETE:
        # Don't allow players to join a game that is over or in progress
        return HttpResponseBadRequest()
        
    for player in request.user.player_set.active():
        # Retire from any game already in progress
        player.leave_game()
        
    # Add player to the new game and redirect to play page.
    game.create_player_for_user(request.user)
    return HttpResponseRedirect(reverse('play-boggle-game', kwargs={'game_id': game.id}))


@login_required
def game_over(request, game_id):
    '''
    Displayed after the maximum number of rounds has been reached.
    '''
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'game': game,
    }
    return render_to_response('boggle/game_over.html', context)


@login_required
def play_game(request, game_id):
    '''
    Play a game of boggle.
    '''
   
    
    game = get_object_or_404(Game, pk=game_id)
    try:
        player = game.player_set.active().get(user=request.user)
    except Player.DoesNotExist:
        # For now, if anything goes wrong just abandone the game without reason
        # TODO: provide user with more info, for example "game is over".
        return HttpResponseRedirect(reverse('game-over', kwargs={'game_id': game.id}))
    context = {
        'title': 'Boggle',
        'game': game,
        'you': player,
        'score': game.round and game.round.score_for(player),
        'players': game.player_set.active(),
        'game_states': game_states,
        'query_string': request.GET.urlencode()
    }
    return render_to_response('boggle/play_game.html', context)


@login_required
def compare_words(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    try:
        player = game.player_set.active().get(user=request.user)
    except Player.DoesNotExist:
        return HttpResponseBadRequest()
    others = game.player_set.active().exclude(user=request.user)

    f = lambda words: set([str(word) for word in words if word.valid])
    my_words = f(player.words)
    common_words = set()
    other_words = set()
    
    for other in others:
        words = f(other.words)
        common_words |= my_words & words
        my_words -= common_words
        other_words |= words - my_words - common_words
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps({
        'my': list(my_words),
        'common': list(common_words),
        'other': list(other_words),
    }))
    return response


@login_required
def submit_score(request, game_id):
    if request.method != 'POST': return HttpResponseBadRequest()
    game = get_object_or_404(Game, pk=game_id)
    try:
        player = game.player_set.active().get(user=request.user)
    except Player.DoesNotExist:
        return HttpResponseBadRequest()
    player.set_round_score(int(request.POST['score']))
    return HttpResponse()


@login_required
def add_word_to_game(request, game_id):
    if request.method != 'POST': return HttpResponseBadRequest()
    game = get_object_or_404(Game, pk=game_id)
    try:
        player = game.player_set.active().get(user=request.user)
    except Player.DoesNotExist:
        return HttpResponseBadRequest()
    word = request.POST['word']
    result = player.add_word(word)
    response = HttpResponse(mimetype='application/json')
    f = lambda value: value and 'true' or 'false'
    response.write('{valid: %s, duplicate: %s, score: %d}'
        % (
            f(result['valid']),
            f(result['duplicate']),
            result['score'],
        ))
    return response


@login_required
def query_game_state(request, game_id):
    game = get_object_or_404(Game, pk=game_id)    
    response = HttpResponse(mimetype='application/json')
    info = {
        'state': game.state,
        'round': game.round and game.round.id or 0,
    }
    response.write(json.dumps(info))
    return response
    

def time_left_in_round(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    response = HttpResponse(mimetype='application/json')
    response.write('%d' % game.round.time_left())
    return response
    
    
@login_required
def reset_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.reset_game()
    return HttpResponseRedirect(reverse('play-boggle-game', kwargs={'game_id': game.id}))
