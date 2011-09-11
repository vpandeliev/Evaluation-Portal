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


def get_online_users(num):
    
    cached_users = cache.get("recent_users_list") or []
    now = datetime.now()
    
    for user in cached_users:
        # If user entry is no longer in the cache, then it has timed out and the
        # user is no longer active. Update the list to reflect this
        if not cache.get(user):
            cached_users.remove(user)
    # save the new user list in the cache.
    cache.set("recent_users_list", cached_users, 16000000)
    
    return cached_users


#@login_required
def basic_test(request):
    test = get_online_users(5)
    
    return render_to_response('basic_test.html', locals(), 
                              context_instance=RequestContext(request))






