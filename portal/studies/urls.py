from django.conf.urls.defaults import *
from portal.studies.views import *

urlpatterns = patterns('',
    url(r'^$', show_many_studies, name="show_many_studies"),
    url(r'^new$', create_one_study, name="create_one_study"),
    url(r'^send-data$', log_game, name="log_game"),   
    url(r'^mark-read$', mark_read, name="mark_read"),   
    url(r'^ic$', informed_consent, name="informed_consent"),
    url(r'^consented$', consented, name="consented"),
    url(r'^datadump$', data_dump, name="data_dump"),
    url(r'^messages$', outbox, name="outbox"),
    # Hosted games
    (r'^boggle/', include('portal.boggle.urls')),
    url(r'^fbog$', finish_boggle_session, name="finish_boggle_session"),
    url(r'^(\d+)/(\d+)$', show_one_study, name="show_one_study"),
    url(r'^edit/(\d+)', edit_one_study, name="edit_one_study"),
    url(r'^remove/(\d+)', remove_one_study, name="remove_one_study"),
    url(r'^add_part/(\d+)', add_participant_to_study, name="add_participant_to_study"),
    url(r'^added_to_study/(\d+)/(\d+)/', added_to_study, name="added_to_study"),
    url(r'^(\d+)/users/', show_users_in_study, name="show_users_in_study"),
    (r'^tinymce/', include('tinymce.urls')), 

)
