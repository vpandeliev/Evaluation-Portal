

#@login_required
def investigator_home(request):
    online_users = get_online_users()
    
    # TODO: only users in an investigator's study
    user_status = []
    for u in User.objects.all():
        # user_info = (username, is_active, has_pending_invite)
        username = u.username
        if cache.get(username):
            user_info = (username, True, has_pending_invite(username))
            user_status.insert(0, user_info)
        else:
            user_info = (username, False, has_pending_invite(username))
            user_status.append(user_info)
        
    request_declined = True if cache.get(request.user.username + "_no_chat_requested") else False
    
    return render_to_response('basic_test.html', locals(), 
                              context_instance=RequestContext(request))

