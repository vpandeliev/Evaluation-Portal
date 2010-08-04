from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#from blank import Blank



############### Study
@login_required
def show_many_studies(request):
    if StudyParticipant.objects.count > 0:
        studies_as_participant = StudyParticipant.objects.filter(user=request.user)
        current_stages = [x.get_current_stage() for x in studies_as_participant]
    else:
        studies_as_participant = []
        current_stages = []

    if StudyInvestigator.objects.count > 0:
        studies_as_investigator = StudyInvestigator.objects.filter(investigator=request.user)
    else:
        studies_as_investigator = []

    return render_to_response('show_many_studies.html', locals(), context_instance=RequestContext(request))

@login_required
def show_one_study(request,as_inv,s_id):
    study_id = int(s_id)
    as_inv = int(as_inv)
    request.session['study_id'] = study_id
    study = Study.objects.get(id=study_id)
    role = study.role(request.user)
    if as_inv == 0 and role >= 0:
        #role >= 0 and as_part == 0
        #participant
        studypart = study.get_study_participant(request.user)
        stages = studypart.participant_stages()
        action = studypart.get_current_stage().stage.url
    elif as_inv == 1 and role <= 0: 
        #investigator
        studyinv = study.get_study_investigator(request.user)
        stages = studyinv.stages()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return render_to_response('show_one_study.html',locals(), context_instance=RequestContext(request))
    
@login_required
def show_users_in_study(request,study_id):
    users = Study.objects.get(id=study_id).participants()
    return render_to_response('show_users.html', locals(), context_instance=RequestContext(request))

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
    return render_to_response('new_study.html', locals(), context_instance=RequestContext(request))
        
@login_required     
def edit_one_study(request,study_id):
    """docstring for edit_one_study"""
    if request.method == 'POST':
        pass #update
    else: #render the form
        study = Study.objects.get(id=study_id)
        form = NewStudyForm(instance=study)
        return render_to_response('edit_study.html',locals(), context_instance=RequestContext(request))

@login_required
def remove_one_study(request,study_id):
    """docstring for remoe_one_study"""
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
            return render_to_response('add_participant_to_study.html',locals(), context_instance=RequestContext(request))
    else: #render the form
        study = Study.objects.get(id=study_id)
        form = AddParticipantForm()
        return render_to_response('add_participant_to_study.html',locals(), context_instance=RequestContext(request))


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
    return render_to_response('added_to_study.html',locals(), context_instance=RequestContext(request))

############### Data Collection

@login_required
def informed_consent(request):
    sid = request.session['study_id']
    study = Study.objects.get(id=sid)
    role = study.role(request.user)
    if role > -1:
        #participant
        studynum = sid
        studypart = study.get_study_participant(request.user)
        stage = studypart.get_current_stage()
        action = stage.stage.url
        if stage.order != 1:
            return HttpResponseBadRequest()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return render_to_response('informed_consent.html',locals(), context_instance=RequestContext(request))


@login_required
def consented(request):
    study_id = int(request.session['study_id'])
    study = Study.objects.get(id=study_id)
    role = study.role(request.user)
    if role > -1:
        #participant
        studypart = study.get_study_participant(request.user)
        stage = studypart.get_current_stage()
        log_consent(request)
        stage.session_completed()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return HttpResponseRedirect('/study/0/'+study_id)

@login_required
def finish_boggle_session(request):
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    role = study.role(request.user)
    if role > -1:
        #participant
        studypart = study.get_study_participant(request.user)
        stage = studypart.get_current_stage()
        stage.session_completed()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return HttpResponseRedirect('/study/0/'+str(study_id))
    
@login_required
def log_game(request):
    """Logs a single piece of data from an in-house game's POST request"""
    if request.method != 'POST': 
        return HttpResponseBadRequest()
    studyid = request.session['study_id']
    timestamp = request.POST['timestamp']
    data = request.POST['data']
    dt = datetime.datetime.fromtimestamp(float(timestamp))
    code = request.POST['code']
    try:
      Data.write(studyid, request.user, dt, data,code)
    except Exception as inst:
      print "log_game:" + inst
    #send: studyid, request.user, time, data
    return HttpResponse("YAY!")

@login_required
def log_consent(request):
    """Logs informed consent"""
    #print "logging consent"
    try:
        Data.write(request.session['study_id'], request.user, datetime.datetime.now(), "Consent given", "CON")
    except Exception as inst:
      print "log_consent", inst
    #send: studyid, request.user, time, data
    return HttpResponse("YAY!")

############### StudyUser

    

def invite_user(request,study_id):
    pass
    
def remove_user(request,study_id,user_id):
    pass


