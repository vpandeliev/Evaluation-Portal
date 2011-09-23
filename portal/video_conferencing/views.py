from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.cache import cache


#################################################################################
#   DJANGO URLS
#################################################################################


def get_online_users():
    """Returns a list of online users that have been recently active."""
    
    cached_users = cache.get("recent_users_dict") or {}
    now = datetime.now()
    
    for username in cached_users.keys():
        # If user entry is no longer in the cache, then it has timed out and the
        # user is no longer active. Update the list to reflect this
        if not cache.get(username):
            del cached_users[username]
            
    # save the new user list in the cache.
    cache.set("recent_users_dict", cached_users, 16000000)
    
    return cached_users


def request_video_chat(request):
    
    # get username from request POST data
    
    # set a cache element that the participants can check when they visit the
    # study page...
    
    # UI: separate tab on study page for 
    pass

#@login_required
def basic_test(request):
    test = get_online_users()
    
    # TODO: only users in an investigator's study
    user_status = U:
        
    
    return render_to_response('basic_test.html', locals(), 
                              context_instance=RequestContext(request))






