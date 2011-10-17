from datetime import datetime
from django.core.cache import cache
from django.conf import settings


#################################################################################
# Useful functions for investigator video conferencing stuff
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
    cache.set("recent_users_dict", cached_users, settings.RECENT_USER_LIST_TIMEOUT)
    
    return cached_users


def has_pending_invite(username):
    """Returns True iff the user with the supplied username has a pending video
    request."""
    if cache.get(username + "_has_pending_invite"):
        return True
    else:
        return False

# 30 second timeout for now...
def set_pending_invite(username):
    """Sets a field in the cache that represents a pending videoconferencing 
    invitation to the user"""
    cache.set(username + "_has_pending_invite", True, settings.VIDEO_INVITE_TIMEOUT)


def uninvite_user(request):
    """Sets a field in the cache that represents a pending videoconferencing 
    invitation to the user"""
    username = request.GET.get("pk", None)
    cache.delete(username + "_has_pending_invite")


def invite_user(request):
    # set a cache element that the participants can check when they visit the
    # study page...
    username = request.GET.get("pk", None)
    set_pending_invite(username)


def decline_video_request(request):
    username = request.GET.get("pk", None)
    cache.delete(username + "_has_pending_invite")
    cache.set(username + "_no_chat_requested", True, settings.VIDEO_REJECTED_TIMEOUT)
    print cache.get(username + "_no_chat_requested")
    






