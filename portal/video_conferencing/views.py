from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from studies.models import UserActivity
from django.core.cache import cache


#################################################################################
#   DJANGO URLS
#################################################################################


def get_online_users(num):
    #one_minute = datetime.now() - timedelta(minutes=1)
    #sql_datetime = datetime.strftime(one_minute, '%Y-%m-%d %H:%M:%S')
    #users = UserActivity.objects.filter(last_activity_date__gte=sql_datetime, user__is_active__exact=1).order_by('-last_activity_date')[:num]
    #return [u.user for u in users]
    
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






