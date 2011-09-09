#
#   Middleware to update the UserActivity database entries whenever a user does
#   pretty much anything.
#
#   Note. This is inefficient as hell. It would be good to use a memache and just
#   update it using this middleware instead of saving datetimes to a database.
#   Need to install some external software for that though...
#
from studies.models import UserActivity
from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site

class UserActivityMiddleware:
    def process_view(self, request, view, args, kwargs):
        if not request.user.is_authenticated():
            return
        
        
        # Only update when the users are in a study doing stuff.
        if request.path.find("study") == -1:
            return
        
        activity = None
        try:
            activity = request.user.useractivity
        except:
            activity = UserActivity()
            activity.user = request.user
            activity.last_activity_date = datetime.now()
            activity.last_activity_ip = request.META['REMOTE_ADDR']
            activity.save()
            return
            
        activity.last_activity_date = datetime.now()
        activity.last_activity_ip = request.META['REMOTE_ADDR']
        activity.save()






  