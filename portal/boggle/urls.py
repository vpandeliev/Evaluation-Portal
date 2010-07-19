from django.conf.urls.defaults import *


urlpatterns = patterns('portal.boggle.views',
    url(r'^games/$', 'index', name='boggle-index'),
    url(r'^games/new/$', 'create_and_join_new_game', name='create-new-boggle-game'),
    url(r'^games/(?P<game_id>\d+)/start/$', 'start_game', name='start-boggle-game'),
    url(r'^games/(?P<game_id>\d+)/next-round/$', 'next_round', name='next-boggle-round'),    
    url(r'^games/(?P<game_id>\d+)/join/$', 'join_game', name='join-boggle-game'),
    url(r'^games/(?P<game_id>\d+)/leave/$', 'leave_game', name='leave-boggle-game'),
    url(r'^games/(?P<game_id>\d+)/play/$', 'play_game', name='play-boggle-game'),
    # XHR
    url(r'^games/(?P<game_id>\d+)/add-word/$', 'add_word_to_game', name='add-word-to-boggle-game'),
    url(r'^games/(?P<game_id>\d+)/time-left/$', 'time_left_in_round', name='time-left-in-boggle-round'),
    url(r'^games/(?P<game_id>\d+)/compare-words/$', 'compare_words', name='compare-words-for-boggle-round'),
    url(r'^games/(?P<game_id>\d+)/submit-score/$', 'submit_score', name='submit-score-for-boggle-round'),
    url(r'^games/(?P<game_id>\d+)/query-state/$', 'query_game_state', name='query-boggle-game-state'),
    # For debugging
    url(r'^games/(?P<game_id>\d+)/reset/$', 'reset_game', name='reset-boggle-game'),
)
