from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
import datetime
from operator import attrgetter


class Study(models.Model):

	name = models.CharField('Study Name', max_length=300)
	description = tinymce_models.HTMLField('Description')
	start_date = models.DateField('Starting Date', blank=True, null=True)
	end_date = models.DateField('End Date', blank=True, null=True)
	started =  models.BooleanField('Started', default=False)
	consent = tinymce_models.HTMLField('Informed Consent Form')
	instructions = tinymce_models.HTMLField('Study Instructions')
	eligibility = tinymce_models.HTMLField('Eligibility Criteria')
	reward = tinymce_models.HTMLField('Compensation and Reward')
	
	def save(self, *args,**kwargs):
		#create timestamps, keep track of user
		
		super(Study, self).save(*args, **kwargs) 
	
	def role(self,user):
		if StudyInvestigator.objects.filter(investigator=user,study=self).count() > 0:
			return 2
		elif StudyParticipant.objects.filter(user=user,study=self).count() > 0:
			return 1
		else:
			return 0
			
	def set_investigator(self, current_user):
		"""Assign creator of study to investigator role"""
		StudyInvestigator(study=self,investigator=current_user).save()

	def participants(self):
		"""Returns a list of all participants in the Study"""
		return [x.user for x in StudyUser.objects.filter(study=self)]

	def investigators(self):
		"""Returns a list of all investigators in the Study"""
		return [x.investigator for x in StudyInvestigator.objects.filter(study=self)]

	def get_study_participant(self, user):
		return StudyParticipant.objects.get(study=self, user=user)

	def get_study_investigator(self, user):
		return StudyInvestigator.objects.get(study=self, investigator=user)

#error checking?
			
	def __unicode__(self):
		return u'%s' % (self.name)

		
	# def __dict__(self):
	# 	"""docstring for __dict__"""
	# 	return {
	# 		'name': self.name,
	# 		'description': self.description,
	# 		'start_date': self.start_date,
	# 		'end_date': self.end_date,
	# 		'started': self.started,
	# 	}

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
		stageusers = [UserStage.objects.filter(stage=x)[0] for x in stages]
		stageusers.sort(key=attrgetter('order'))
		return [x.stage for x in stageusers]
		#return [11,22,33]
			

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
		return UserStage.objects.get(user=self.user, status=1)
		

			
	def __unicode__(self):
		return u'%s - %s (Participant)' % (self.user,self.study)		


		
class Stage(models.Model):
	name = models.CharField('Stage Name', max_length=300)
	study = models.ForeignKey(Study)
	sessions = models.IntegerField('Number of sessions')
	deadline = models.IntegerField('Time to finish session (in days)')
	url = models.CharField('Stage URL', max_length=300)
	description = tinymce_models.HTMLField('Stage Description')
	instructions = tinymce_models.HTMLField('Stage Instructions')

	def __unicode__(self):
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
	
#	def stages_in_group(self, group):
#		"""docstring for stages_in_group"""
#		return [x.stage for x in StageGroup.objects.filter(group=group).order_by('order')]
	
	def __unicode__(self):
		return u'%s - %s (%s)' % (self.stage, self.group, self.order)

class Data(models.Model):
    """A data object"""
    
    studyparticipant = models.ForeignKey(StudyParticipant)
    stage = models.IntegerField('Stage')
    session = models.IntegerField('Session')
    timestamp = models.DateTimeField('Timestamp')
    datum = models.TextField('Datum')
    
    @classmethod
    def write(cls,studyid, user, time, data):
        d = Data()
        d.studyparticipant = Study.objects.get(id=int(studyid)).get_study_participant(user) 
        stage = d.studyparticipant.get_current_stage()
        d.stage = stage.order
        d.session = stage.sessions_completed + 1
        d.timestamp = datetime.datetime.fromtimestamp(float(time))
        d.datum = data
        d.save()
    
        
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
		if sessions_completed == self.stage.sessions:
			#this stage is finished
			self.status = 0
			self.end_date = datetime.datetime.now()
			#find next stage
			next = UserStage.objects.filter(user=self.user, order=self.order+1)
			if len(next) == 0:
				#end of study
				pass
			else:
				next[0].status = 1
				next[0].start_date = datetime.datetime.now()			
		
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
