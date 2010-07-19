'''
Models for storing the game state of Boggle.
'''
#SPPENERZDSEVONTC


import datetime, re
from django.db import models
from django.db.models.signals import *
from django.contrib.auth.models import User
from django.utils.dateformat import format as date_format
from choices import *
from logic import *
from words import english


class GameStateManager(models.Manager):
    '''
    Manager for the current game state.
    '''
    pass
    

class Game(models.Model):
    '''
    Game state and history for the game of Boggle.
    '''
    state = models.PositiveIntegerField(choices=game_states.as_choices(), default=game_states.WAITING_FOR_PLAYERS)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    round_max = models.IntegerField()
    game_over_url = models.CharField(max_length=200)

    round = property(lambda self: self.state == game_states.IN_PROGRESS and self.round_set.count() and self.round_set.all()[0] or None)
    board = property(lambda self: self.state == game_states.IN_PROGRESS and self.round_set.count() and Board(self.round.board) or None)
    is_over = property(lambda self: self.round_set.count() >= self.round_max)

    class Meta:
        ordering = ['-created_at']
    
    objects = GameStateManager()

    def __unicode__(self):
        return unicode(self.id)

    def start_round(self, mode):
        '''
        Args:
            mode - See portal.boggle.choices.boggle_modes
        '''
        assert self.state == game_states.WAITING_FOR_PLAYERS, 'This game has already been started!'
        assert self.player_set.count() >= 1, 'Not enough players to start a game!'
        self.state = game_states.IN_PROGRESS
        self.goto_next_round(mode=mode)
        self.save()

    def goto_next_round(self, mode):
        assert self.state == game_states.IN_PROGRESS, 'Trying to create a new round for a game that is not in progress!'
        self.round_set.create(mode=mode)
    
    def end_round(self):
        assert self.state != game_states.COMPLETE, 'Trying to end a game that is already over!'
        self.state = game_states.COMPLETE
        self.save()
    
    def create_player_for_user(self, user):
        '''
        Adds a user to a game, creating a player who is next in the turn order.
        If an inactive player already exists for this game, that player is
        reactivated instead of creating a new one.
        '''
        try:
            player = self.player_set.get(user=user)
            player.active = True
            player.save()
        except Player.DoesNotExist:
            player = self.player_set.create(user=user)
        if self.round and player.wordlist_set.filter(round=self.round).count() == 0:
            # Add the player to the round if any
            self.round.wordlist_set.create(player=player)
        return player

    def reset_game(self):
        self.state = game_states.WAITING_FOR_PLAYERS
        self.round_set.all().delete()
        self.start_round()

    
class RoundManager(models.Manager):
    
    def __repr__(self):
        return '%d rounds' % self.get_query_set().count()


class Round(models.Model):
    '''
    A game of boggle is a sequence of rounds.
    '''
    game = models.ForeignKey(Game)
    number = models.PositiveIntegerField(blank=True, help_text='Round numbering starts at 1.')
    board = models.TextField(blank=True, help_text='Record of values for each cell in the board. The board is a 4 x 4 grid.')
    start = models.DateTimeField(default=datetime.datetime.now, help_text='Start time of the game.')
    duration = models.PositiveIntegerField(default=180, help_text='Duration of round in seconds.')
    mode = models.PositiveIntegerField(choices=boggle_modes.as_choices())

    objects = RoundManager()
    
    class Meta:
        ordering = ['-number']
    
    def __unicode__(self):
        return self.board

    def is_valid_word(self, word):        
        return word.lower() in english
    
    def score_for(self, player):
        try:
            return self.wordlist_set.get(player=player).score()
        except WordList.DoesNotExist:
            return 0

    def time_left(self):
        '''
        Time left in the round.
        '''
        delta = datetime.timedelta(seconds=self.duration)
        end = self.start + delta
        now = datetime.datetime.now()
        return end > now and (end - now).seconds or 0


def shuffle_board_and_set_round_number(sender, instance, **kwargs):
    if instance.number is None:
        # Shuffle the dice and set the board cell values
        # ...
        instance.board = shuffler[instance.mode]()

        # Set round number
        previous_round = instance.game.round
        instance.number = previous_round and (previous_round.number + 1) or 1
pre_save.connect(shuffle_board_and_set_round_number, sender=Round)


def create_wordlists(sender, instance, **kwargs):
    if not instance.wordlist_set.count():
        # Create new wordlists for each player
        for player in instance.game.player_set.active():
            instance.wordlist_set.create(player=player)
post_save.connect(create_wordlists, sender=Round)
    

class PlayerManager(models.Manager):

    def active(self):
        '''
        Return active players in games which are in progress.
        '''
        return self.get_query_set().filter(active=True, game__state__lte=game_states.IN_PROGRESS)

    def __repr__(self):
        return ', '.join([p.user.username for p in self.get_query_set()])


class Player(models.Model):
    '''
    Game state associated with each player.
    '''
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    position = models.PositiveIntegerField(blank=True, help_text='Players take turns in order by positions. Positioning starts at 1.')
    score = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, help_text='Is the player still playing?')

    objects = PlayerManager()
    
    def _words(self):
        word_list = self._get_word_list()
        return word_list and word_list.words
    words = property(_words)

    class Meta:
        ordering = ['position']
    
    def __unicode__(self):
        return self.user.username

    def _get_word_list(self):
        round = self.game.round
        return round and WordList.objects.get(player=self, round=round) or None

    def set_round_score(self, score):
        word_list = self._get_word_list()
        word_list.final_score = score
        word_list.save()

    def get_game_score(self):
        qs = WordList.objects.filter(player=self, final_score__isnull=False)
        return qs.count() and qs.aggregate(models.Sum('final_score'))['final_score__sum'] or 0

    def add_word(self, word):
        word_list = self._get_word_list()
        assert word_list
        return word_list.add_word(word)

    def leave_game(self):
        self.active = False
        self.save()


def adjust_game_state(sender, instance, **kwargs):
    if not instance.active and instance.game.player_set.active().count() == 0:
        instance.game.end_round()
post_save.connect(adjust_game_state, sender=Player)


def set_player_position(sender, instance, **kwargs):
    if instance.position is None:
        other_players = instance.game.player_set.all()
        n = other_players.count()
        if n > 0:
            instance.position = other_players[n - 1].position
        else:
            instance.position = 1
pre_save.connect(set_player_position, sender=Player)


class Word(object):
    def __init__(self, value):
        self.valid = value[0] == '.'
        self.duplicate = value[1] == '!'
        m = re.match(r'^[.!]{2}\((\d+)\)([A-Z]*)$', value)
        self.score = int(m.group(1))
        self._word = m.group(2)
    def __str__(self):
        return self._word
    def __unicode__(self):
        return self._word
    def __repr__(self):
        return self._word
    def __cmp__(self, other):
        return cmp(self._word, unicode(other))


class WordList(models.Model):
    '''
    A player's word list for a single round of a game.
    '''
    player = models.ForeignKey(Player)
    round = models.ForeignKey(Round)
    raw_words = models.TextField(blank=True)
    final_score = models.PositiveIntegerField(blank=True, null=True)

    def _words(self):
        return map(Word, filter(bool, self.raw_words.split('\n')))
        # return [word[1:] for word in self.raw_words.split('\n') if word.startswith('.')]
    words = property(_words)

    def __unicode__(self):
        return self.raw_words[:20].replace('\n', ' ').replace('\r', ' ')

    def add_word(self, word):
        valid = self.round.is_valid_word(word)
        duplicate = word in self.words
        score = scoring[self.round.mode](word)
        score = (not duplicate and valid) and score or 0
        
        self.raw_words = (
            (not valid and '!' or '.')
            + (duplicate and '!' or '.')
            + ('(%d)' % score)
            + self.normalize_word(word) + '\n'
            + self.raw_words
            )
        self.save()
        return {
            'valid': valid,
            'duplicate': duplicate,
            'score': score,
            }
    
    def score(self):
        return sum([word.score for word in self.words])
        
    @staticmethod
    def normalize_word(word):
        return word.upper()
