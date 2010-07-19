from django.contrib import admin
from models import *


class RoundInline(admin.TabularInline):
    model = Round
    fields = ('number', 'board', 'start', 'duration', 'mode')
    extra = 0

class PlayerInline(admin.TabularInline):
    model = Player
    fields = ('user', 'position', 'score', 'active')
    extra = 0
    
class GameAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('created_at', 'state', 'round_max', 'game_over_url')}),
        )
    list_display = ('id', 'created_at', 'state', 'round_set', 'round_max', 'player_set')
    list_filter = ('state',)
    date_hierarchy = 'created_at'
    search_fields = ('player__user__username', 'round__wordlist__raw_words')
    inlines = [PlayerInline, RoundInline]
admin.site.register(Game, GameAdmin)

class WordListInline(admin.TabularInline):
    model = WordList
    fields = ('player', 'raw_words', 'final_score')
    extra = 1

class RoundAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('game', 'number', 'board', 'start', 'duration', 'mode')}),
        )
    list_filter = ('game',)
    list_display = ('board', 'game', 'number', 'start', 'duration', 'mode')
    date_hierarchy = 'start'
    search_fields = ('wordlist__raw_words',)
    inlines = [WordListInline]
admin.site.register(Round, RoundAdmin)
