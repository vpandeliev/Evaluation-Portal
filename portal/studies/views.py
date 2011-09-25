from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from context_processors import *
import datetime
from django.core.cache import cache


############### Study


@login_required
def show_many_studies(request):
    if StudyParticipant.objects.count > 0:
        studies_as_participant = StudyParticipant.objects.filter(user=request.user)
        current_stages = UserStage.objects.filter(user=request.user, status=1)
        
    else:
        studies_as_participant = []
        current_stages = []

    if StudyInvestigator.objects.count > 0:
        studies_as_investigator = StudyInvestigator.objects.filter(investigator=request.user)
    else:
        studies_as_investigator = []
    
    #part = len(studies_as_participant)
    #inv = len(studies_as_investigator)
    
    #if part+inv == 1:
    #    if part > inv:
    #        return show_one_study(request, 0, studies_as_participant[0].study.id)
    #    else:
    #        return show_one_study(request, 1, studies_as_investigator[0].study.id)
        
    return render_to_response('study/show_many_studies.html', locals(), context_instance=RequestContext(request))


@login_required
# TODO: get rid of 90% of this... can do everything just from the request object
#       since login is required (must be able to quickly get what you want by
#       username alone, so a couple things will need to be changed to implement
#       this)
def show_one_study(request,as_inv,s_id):
    study_id = int(s_id)
    as_inv = int(as_inv)
    request.session['study_id'] = study_id
    study = Study.objects.get(id=study_id)
    role = study.role(request.user)
    video_request = True if cache.get(request.user.username + "_has_pending_invite") else False
    username = request.user.username
    
    if as_inv == 0 and role >= 0:
        #role >= 0 and as_part == 0
        #participant
        studypart = study.get_study_participant(request.user)
        stages = UserStage.objects.filter(user=request.user, study=study)
        #stages = studypart.participant_stages()
        current_stage = studypart.get_current_stage()
        if current_stage:
            action = current_stage.stage.url
        else:
            action = "study/show_many_studies"
            
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    
    return render_to_response('study/show_one_study.html',locals(), context_instance=RequestContext(request))


@login_required
def show_users_in_study(request,study_id):
    users = Study.objects.get(id=study_id).participants()
    return render_to_response('study/show_users.html', locals(), context_instance=RequestContext(request))


@login_required
def create_one_study(request):
    if request.method == 'POST':
        form = NewStudyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            s = Study.objects.create(
                name=cd['name'],
                start_date=cd['start_date'],
                end_date=cd['end_date'],
                started=cd['started'],
                description=cd['description'])
            s.set_investigator(request.user)
            return HttpResponseRedirect('/study/'+str(s.id))
    else:
        #study = Blank()
        form = NewStudyForm()
    return render_to_response('study/new_study.html', locals(), context_instance=RequestContext(request))


@login_required
def edit_one_study(request,study_id):
    """docstring for edit_one_study"""
    if request.method == 'POST':
        pass #update
    else: #render the form
        study = Study.objects.get(id=study_id)
        form = NewStudyForm(instance=study)
        return render_to_response('study/edit_study.html',locals(), context_instance=RequestContext(request))


@login_required
def remove_one_study(request,study_id):
    """docstring for remove_one_study"""
    s = Study.objects.get(id=study_id)
    StudyParticipant.objects.filter(study=s).delete()
    StudyInvestigator.objects.filter(study=s).delete()
    
    s.delete()
    return HttpResponseRedirect('/study/')


@login_required
def add_participant_to_study(request,study_id):
    """docstring for add_participant_to_study"""
    if request.method == 'POST':
        newuser = False
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            study = Study.objects.get(id=study_id)
            query = cd['email']
            user = User.objects.filter(email=query)
            
            if len(user) == 0:
                newuser = True
                pwd = hashlib.new('ripemd160')
                pwd.update(cd['email'])
                pwd = pwd.hexdigest()[:10]
                user = User.objects.create_user(username=cd['email'],email=cd['email'],password=pwd)
                user.message_set.create(message=pwd)
            else:
                user = user[0]
            #study.set_investigator(user)
            #add participant to study
            create_user_stages(user)
            return HttpResponseRedirect('/study/added_to_study/'+ str(user.id)+"/"+str(study.id))
        else:
            return render_to_response('study/add_participant_to_study.html',locals(), context_instance=RequestContext(request))
    else: #render the form
        study = Study.objects.get(id=study_id)
        form = AddParticipantForm()
        return render_to_response('study/add_participant_to_study.html',locals(), context_instance=RequestContext(request))


@login_required
def added_to_study(request, study_id, user_id):
    """docstring for added_to_study"""
    useradded = User.objects.get(id=user_id)
    study = Study.objects.get(id=study_id)

    message = useradded.get_and_delete_messages()
    if len(message) == 0 :
        message = None
    else:
        message = message[0]
    new = not (message is None)
    return render_to_response('study/added_to_study.html',locals(), context_instance=RequestContext(request))


############### Data Collection


@login_required
def informed_consent(request):
    sid = request.session['study_id']
    study = Study.objects.get(id=sid)
    role = study.role(request.user)
    if role > -1:
        #participant
        
        # CLEANUP: this chain of lookups seems unnecessary
        studynum = sid
        studypart = study.get_study_participant(request.user)
        stage = studypart.get_current_stage()
        action = stage.stage.url
        if stage.order != 1:
            return HttpResponseBadRequest()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return render_to_response('study/informed_consent.html',locals(), context_instance=RequestContext(request))


@login_required
def questionnaire(request):
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            log(request,"QUE",cd)
            return HttpResponseRedirect('/study/0/'+ str(request.session['study_id']))
    else:
        form = QForm()
    return render_to_response('study/questionnaire.html', {'form': form, 'button': 'Submit'})


@login_required
def consented(request):
    study_id = int(request.session['study_id'])
    study = Study.objects.get(id=study_id)
    role = study.role(request.user)
    if role > -1:
        #participant
        studypart = study.get_study_participant(request.user)
        stage = studypart.get_current_stage()
        log(request, "CON", "Consent Given")
        stage.session_completed()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return HttpResponseRedirect('/study/0/'+str(study_id))


@login_required
def data_dump(request,study_id):
    #study_id = int(request.session['study_id'])
    study = Study.objects.get(id=study_id)
    study_participants = StudyParticipant.objects.filter(study=study)
    role = study.role(request.user)
    if role < 1:
        #investigator
        dumpfile = "data/data_study_" + str(study_id) + ".csv"
        data = []
        for x in study_participants:
            obj = Data.objects.filter(studyparticipant=x)
            for y in obj:
                data.append(y.data())
        FILE = open(dumpfile, "w")
        FILE.write("username,studyid,stage,stageslug,session,year,month,day,hour,minute,second,millisecond,code,datum\n")
        for line in data:
            FILE.write(line + "\n")
        FILE.close()
        FILE = open(dumpfile, "r")
        datadump = ""
        linelist = FILE.readlines()
        for x in linelist:
            datadump = datadump + x + "<br/>"
            
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    #return HttpResponseRedirect('/study/1/'+str(study_id))
    return render_to_response("data.html", locals(), context_instance=RequestContext(request))


@login_required
def choose_assess(request):
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    sp = StudyParticipant.objects.get(user=request.user, study=study)
    us = sp.get_current_stage()
    sc = us.sessions_completed
    us.start_stage()
    if sc%2 == 0:
        return HttpResponseRedirect('/study/assess/setswitch')
    else:
        return HttpResponseRedirect('/study/assess/flanker')


@login_required
def choose_task(request):
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    sp = StudyParticipant.objects.get(user=request.user, study=study)
    us = sp.get_current_stage()
    sc = us.sessions_completed
    us.start_stage()
    if sc%2 == 0:
        return HttpResponseRedirect('/study/fitbrains/0')
    else:
        return HttpResponseRedirect('/study/fitbrains/1')


@login_required
def show_task(request, game):
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    sp = StudyParticipant.objects.get(user=request.user, study=study)
    stage = sp.get_current_stage()
    sde = study.task_session_dur
    elapsed = datetime.datetime.now() - stage.curr_session_started
    sd = sde - elapsed.seconds / 60
    if game == '1':
        gametitle = "Wonder-Juice Machine"
        link = "wonder_juice_machine"
        code = "WDJ"
    else:
        gametitle = "Paradise Island II"
        link = "paradise_island"
        code = "PAR"
    return render_to_response('study/fitbrains.html', locals(),context_instance=RequestContext(request))



@login_required
def show_wonderjuice(request):
    return render_to_response('study/wonderjuice.html', context_instance=RequestContext(request))



@login_required
def finish_session(request):
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    role = study.role(request.user)
    if role > -1:
        #participant
        studypart = StudyParticipant.objects.get(study=study,user=request.user)
        #stage = studypart.get_current_stage()
        stage = UserStage.objects.get(user=request.user, study=study, status=1)
        stage.session_completed()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return HttpResponseRedirect('/study/0/'+str(study_id))
    

@login_required
def finish_task(request,code):
    log(request,code,"Task Finished")
    return HttpResponseRedirect('/study/fsess')



# CLEANUP: How do we want to let the user customize /deal with data collection?
@login_required
def save_post_data(request):
    """Saves arbitrary POST data from a user stage and responds with a 
    confirmation."""
    
    if request.method != 'POST': 
        return HttpResponse("not_post")
        
    studyid = request.session['study_id']
    
    # Save in comma separated value format
    data = ""
    for key in request.POST:
        data = data + "{0},{1}\n".format(key, request.POST[key])
    
    print data
    
    dt = datetime.datetime.now()    
    code = "CSV"

    try:
        Data.write(studyid, request.user, dt, code, data)
    except Exception:
        return HttpResponse("couldn't save")
        
    #send: studyid, request.user, time, data
    return HttpResponse("success")


@login_required
def log_game(request):
    """Logs a single piece of data from an in-house game's POST request"""

    if request.method != 'POST': 

        return HttpResponseBadRequest()
        
    studyid = request.session['study_id']
    user = request.user
    timestamp = datetime.datetime.now()
    data = request.POST['data'] # CLEANUP: This is the user's data. Think about how to let them change this...
    code = request.POST['code']
    
    try:
        Data.write(studyid, user, timestamp, code, data)
    except Exception:
        HttpResponse(content='FAILED', mimetype=DEFAULT_CONTENT_TYPE)

    # User should read this using an ajax request before calling fsess
    return HttpResponse(content="SUCCESS")



@login_required
def log(request, code, datum):
    """Logs things"""
    #print "logging"
    studyid = request.session['study_id']
    
    try:
        Data.write(studyid, request.user, datetime.datetime.now(), code, datum)
    except Exception:
      print "logging: failed"
     #send: studyid, request.user, time, data
    return HttpResponse("YAY!")


@login_required
def mark_read(request):
    """Marks a message with a particular ID as read"""
    if request.method != 'POST': 
        return HttpResponseBadRequest()
    print "mark read", request.POST['id']

    msgid = int(request.POST['id'])
    
    msg = AlertRecepient.objects.get(id=msgid)
    #usermsg = AlertRecepient.objects.get(alert=msg, recepient=request.user)
    msg.read = 1
    msg.save()
    return HttpResponse("YAY!")

@login_required
def send_alert(request):
    """Sends a message"""
    if request.method != 'POST': 
        return HttpResponseBadRequest()
    #print request.POST
    #create alert
    try:
        a = Alert.create(request.POST['subject'], request.POST['body'], request.user)
    except Exception:
        print "Alert failed to create"
    
    recepients = request.POST.getlist('participants')
    
    
    for x in recepients:
        #print x, "gets", request.POST.get['body']
        print x, "gets", request.POST['body']
        AlertRecepient.associate(a, x)
        #make alertrecepients
    return HttpResponse("YAY!")




############### StudyUser
def invite_user(request,study_id):
    pass
    
def remove_user(request,study_id,user_id):
    pass


