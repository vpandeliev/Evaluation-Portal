from django.db import models

from django.contrib.auth.models import User
from tinymce import models as tinymce_models
import datetime
from operator import attrgetter




class Study(models.Model):

    name = models.CharField('Study Name', max_length=300)
    stub = models.CharField('Study Stub', max_length=3)
    description = tinymce_models.HTMLField('Description')
    start_date = models.DateField('Starting Date', blank=True, null=True)
    end_date = models.DateField('End Date', blank=True, null=True)
    started =  models.BooleanField('Started', default=False)
    consent = tinymce_models.HTMLField('Informed Consent Form')
    instructions = tinymce_models.HTMLField('Study Instructions')
    eligibility = tinymce_models.HTMLField('Eligibility Criteria')
    reward = tinymce_models.HTMLField('Compensation and Reward')
    
    #added to customize durations
    task_session_dur = models.IntegerField("Session Duration (minutes)")
    assess_blocks = models.IntegerField("Number of assessment blocks")
    assess_trials = models.IntegerField("Number of trials per block")
    
    
    def save(self, *args,**kwargs):    
        #create timestamps, keep track of user
        super(Study, self).save(*args, **kwargs) 
    
    
    def role(self,user):
        a = 0
        allowed = False
        if StudyParticipant.objects.filter(user=user,study=self).count() > 0:
            a += 1
            allowed = True
        if StudyInvestigator.objects.filter(investigator=user,study=self).count() > 0:
            a += -1
            allowed = True
        if allowed:
            return a
        else:
            return -2
    
    
    def set_investigator(self, current_user):
        """Assign creator of study to investigator role"""
        StudyInvestigator(study=self,investigator=current_user).save()
    
    
    def participants(self):
        """Returns a list of all participants in the Study"""
        return [x.user for x in StudyParticipant.objects.filter(study=self)]
    
    
    def investigators(self):
        """Returns a list of all investigators in the Study"""
        return [x.investigator for x in StudyInvestigator.objects.filter(study=self)]
    
    
    def get_study_participant(self, user):
        s = StudyParticipant.objects.get(study=self, user=user)
        return s
    
    
    def get_study_investigator(self, user):
        return StudyInvestigator.objects.get(study=self, investigator=user)
    
    
    def __unicode__(self):
        return u'%s' % (self.name)


class Group(models.Model):
    name = models.CharField('Group Name', max_length=300)
    study = models.ForeignKey(Study)
    
    
    def __unicode__(self):
        return u'%s - %s' % (self.study, self.name)     
    
    
    def stages(self):
        return [x.stage for x in StageGroup.objects.filter(group=self).order_by('order')]


class StudyInvestigator(models.Model):
    study = models.ForeignKey(Study)
    investigator = models.ForeignKey(User)
    
    
    def stages(self):
        """Returns all of a study's stages as userstage objects"""
        stages = Stage.objects.filter(study=self.study)
        stageusers = [StageGroup.objects.filter(stage=x)[0] for x in stages]
        stageusers.sort(key=attrgetter('order'))
        return [x.stage for x in stageusers]
    
    
    def stages_per_condition(self, cond):
        return StageGroup.objects.filter(group=cond).order_by('order')
    
    
    def __unicode__(self):
        return u'%s - %s (Investigator)' % (self.investigator.username, self.study)


class StudyParticipant(models.Model):
    study = models.ForeignKey(Study)
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    
    #CHOICES = ((1, 'Investigator'),(0, 'Participant'))
    #role = models.IntegerField("Role", max_length=1, choices=CHOICES)
    #current_condition = models.ForiengKey(Condition)
    
    #current_stage = models.IntegerField('Current Stage', default=1)
    #current_session = models.IntegerField('Current Session', default=1)
    #last_action = models.DateTimeField('Last Session Completed')

    def participant_stages(self):
        return UserStage.objects.filter(user=self.user).order_by('order')

    def number_of_stages(self):
        return self.participant_stages().count()
        
    def save(self):
        #create timestamps, keep track of user modifying, etc.
        super(StudyParticipant,self).save()

    def get_current_stage(self):
        #get the current userstage object
        try:
            current_stage = UserStage.objects.get(user=self.user, study=self.study, status=1)
        except UserStage.DoesNotExist:
            current_stage = None
            
        return current_stage
        
        
    #def get_current_stages(self):
        #get the current userstage object
     #   return UserStage.objects.get(user=self.user, status=1)
     
    def __unicode__(self):
        return u'%s - %s (Participant)' % (self.user,self.study)        
    
    def log(self):
        return u'%s,%s' % (self.user.username,self.study.stub)

        
class Stage(models.Model):
    name = models.CharField('Stage Name', max_length=300)
    stub = models.CharField('Stage Stub', max_length=3)
    study = models.ForeignKey(Study)
    sessions = models.IntegerField('Number of sessions')
    deadline = models.IntegerField('Time to finish session (in days)')
    url = models.CharField('Stage URL', max_length=300)
    description = tinymce_models.HTMLField('Stage Description')
    instructions = tinymce_models.HTMLField('Stage Instructions')

    def __unicode__(self):
        return unicode("%s (%s)" % (self.name, self.study.stub))       

    def display(self):
        return unicode(self.name)
        
    def avg(self):
        """docstring for avg"""
        stagegroups = StageGroup.objects.filter(stage=self)
        total = 0
        for x in stagegroups:
            total += x.order
        return total/len(stagegroups)
    
    def number_of_users(self):
        return self.users().count()
    
    
        
    def users(self):
        
        return UserStage.objects.filter(stage=self, status=1).order_by('user')
            
class StageGroup(models.Model):
    group = models.ForeignKey(Group)
    stage = models.ForeignKey(Stage)
    order = models.IntegerField()
    
    @classmethod
    def stages_in_group(cls, group):
        """docstring for stages_in_group"""
        return [x.stage for x in StageGroup.objects.filter(group=group).order_by('order')]
    
    def __unicode__(self):
        return u'%s - %s (%s)' % (self.stage, self.group, self.order)

class Data(models.Model):
    """A data object"""
    
    studyparticipant = models.ForeignKey(StudyParticipant)
    stage = models.IntegerField('Stage')
    stage_stub = models.CharField(max_length=3)
    session = models.IntegerField('Session')
    timestamp = models.DateTimeField('Timestamp')
    datum = models.TextField('Datum')
    code = models.CharField(max_length=3)
    
    @classmethod
    def write(cls, studyid, user, time, code, data):
        d = Data()
        d.studyparticipant = Study.objects.get(id=studyid).get_study_participant(user) 
        astage = d.studyparticipant.get_current_stage()
        d.stage = astage.order

        d.stage_stub = d.studyparticipant.get_current_stage().stage.stub
        d.session = astage.sessions_completed + 1
        d.timestamp = time
        d.datum = data
        d.code = code        
        d.save()
    
    def __unicode__(self):
        return u'%s,%s,%s,%s,%s,%s,%s' % (self.studyparticipant.log(), self.stage, self.stage_stub, self.session, self.format_timestamp(), self.code, self.datum)
        
    def data(self):
        return u'%s,%s,%s,%s,%s,%s,%s' % (self.studyparticipant.log(), self.stage, self.stage_stub, self.session, self.format_timestamp(), self.code, self.datum)

    def format_timestamp(self):
        t = self.timestamp
        return u'%s,%s,%s,%s,%s,%s,%s' % (t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond/1000)


class UserStage(models.Model):
    user = models.ForeignKey(User)
    stage = models.ForeignKey(Stage)
    order = models.IntegerField('Order', editable=False)
    CHOICES = ((0, 'Completed'),(1, 'Active'),(2, 'Future'))
    status = models.IntegerField('Status', max_length=1, choices=CHOICES)
    start_date = models.DateTimeField('Start date', blank=True, null=True)
    end_date = models.DateTimeField('End date', blank=True, null=True)
    sessions_completed = models.IntegerField('Sessions completed')
    last_session_completed = models.DateTimeField('Last session completed', blank=True, null=True)
    curr_session_started = models.DateTimeField('Current session started', blank=True, null=True)
    study = models.ForeignKey(Study)

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.user, self.stage, self.order)

    def save(self, *args,**kwargs):
        super(UserStage, self).save(*args, **kwargs)
        #self.set_order()
            
    def group(self):
        return StudyParticipant.objects.get(user=self.user).group       

    def session_completed(self):
        self.sessions_completed += 1
        self.last_session_completed = datetime.datetime.now()
        Data.write(self.study.id, self.user, self.last_session_completed, "SSC", "Session Completed")
        if self.sessions_completed == self.stage.sessions:
            #this stage is finished
            self.status = 0
            self.end_date = datetime.datetime.now()
            #find next stage
            try:
                next = UserStage.objects.get(user=self.user, study=self.study, order=self.order+1)
                next.status = 1
                next.start_date = datetime.datetime.now()
                next.last_session_completed = next.start_date
                next.save()
            except UserStage.DoesNotExist:
                #end of study
                pass
                
        self.save()       

    def stage_completed(self):
        self.sessions_completed = self.stage.sessions
        self.last_session_completed = datetime.datetime.now()
        Data.write(self.study.id, self.user, self.last_session_completed, "session completed", "ssc")
        self.status = 0
        self.end_date = datetime.datetime.now()
        #find next stage
        next = UserStage.objects.get(user=self.user, order=self.order+1)
        if len(next) == 0:
            #end of study
            pass
        else:
            next.status = 1
            next.start_date = datetime.datetime.now()
            next.save()
        self.save()       

    def start_stage(self):
        self.curr_session_started = datetime.datetime.now()
        self.save()
        
    def set_order(self):
        self.order = StageGroup.objects.get(group=self.group(), user=self.user).order
        
    def users_in_stage(self, stage_object):
        return UserStage.objects.filter(stage=stage_object, status=1)

    def number_users_in_stage(self, stage_object):
        """docstring for number_users_in_stage"""
        return len(self.users_in_stage(stage_object))

    def nextdeadline(self):
        ahead = datetime.timedelta(days=self.stage.deadline)
        return self.last_session_completed + ahead
        
    def overdue(self):
        if datetime.datetime.now() > self.nextdeadline():
            return True
        return False        


class Alert(models.Model):
    """A message object"""

    subject = models.CharField(max_length=80)
    date = models.DateField('Date sent')
    text = models.CharField('Message Text', max_length=350)
    author = models.ForeignKey(User)
    
    def __unicode__(self):
        """docstring for __unicode__"""
        return u'%s - %s' % (self.subject, self.date)
        
    def recepients(self):
        """docstring for recepients"""
        alert_recepients = [x.recepient for x in AlertRecepient.objects.filter(alert=self)]
        return alert_recepients
        
    def recepients_text(self):
        return ','.join(self.recepients())

    @classmethod
    def create(cls, subj, content, sender):
        """docstring for create"""

        a = Alert()
        a.subject = subj
        a.text = content
        a.date = datetime.datetime.now()
        a.author = sender
        a.save()
        return a
        
class AlertRecepient(models.Model):
    """Join b/w messages and recepients"""
    
    recepient = models.ForeignKey(User)
    alert = models.ForeignKey(Alert)
    CHOICES = ((0, 'Unread'),(1, 'Read'))
    read = models.IntegerField('Read?', max_length=1, choices=CHOICES)

    def __unicode__(self):
        """docstring for __unicode__"""
        prefix = ""
        if self.read == 0:
            prefix = "UN"
            
        return u'%s - %s (%sREAD)' % (self.recepient, self.alert.subject, prefix)

    @classmethod
    def associate(cls, a, r):
        """docstring for associate"""
        ar = AlertRecepient()
        ar.alert = a
        ar.recepient = User.objects.get(id=r)
        ar.read = 0
        ar.save()
        
    