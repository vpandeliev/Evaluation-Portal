#
#   Middleware to update the UserActivity database entries whenever a user does
#   pretty much anything.
#
#   Note. This is inefficient as hell. It would be good to use a memache and just
#   update it using this middleware instead of saving datetimes to a database.
#   Need to install some external software for that though...
#
from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache

class UserActivityMiddleware:
    def process_view(self, request, view, args, kwargs):
        if not request.user.is_authenticated():
            return
        
        # Only update when the users are in a study doing stuff.
        if request.path.find("study") == -1:
            return
        
        # TESTING: memory cache for saving active users.
        user_list_timeout = 160000000
        cached_users = cache.get("recent_users_dict")
        username = request.user.username
        if not cached_users:
            cached_users = {username:1}
        else:
            cached_users[username] = 1
        
        cache.set("recent_users_dict", cached_users, user_list_timeout)
        
        # Users time out after 30 seconds. 
        # TODO: make this a parameter in the settings.py file!!!!!!
        cache.set(username, 1, 30)
        





  