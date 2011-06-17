from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

import datetime

#@login_required
def list_users_for_video(request):
   
    user_data = []
    for u in User.objects.all():
        user_data.append( (u.username, u.pk, u.get_profile().has_pending_request) )
    
    return render_to_response('video/video_admin.html', locals(), context_instance=RequestContext(request))


#@login_required
def invite_user(request):
    user_to_invite = request.GET.get("pk", None)
    
    if user_to_invite:
        user = User.objects.get(pk=user_to_invite)
        profile = user.get_profile()
        print dir(profile)#.has_pending_request)
        setattr(profile, 'has_pending_request', 1)
        profile.save()
    
    response = HttpResponse(mimetype='text/html')
    response.write(str(user_to_invite))
    
    return response


#@login_required
def uninvite_user(request):
    user_to_uninvite = request.GET.get("pk", None)

    if user_to_uninvite:
        user = User.objects.get(pk=user_to_uninvite)
        profile = user.get_profile()
        print dir(profile)#.has_pending_request)
        setattr(profile, 'has_pending_request', 0)
        profile.save()

    response = HttpResponse(mimetype='text/html')
    response.write(str(user_to_uninvite))

    return response
