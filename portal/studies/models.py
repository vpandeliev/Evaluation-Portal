from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
import datetime

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
		#print "saving..."
		super(Study, self).save(*args, **kwargs) 
		if Group.objects.filter(name="Investigator", study=self).count() == 0:
			Group.objects.create(name="Investigator", study_id=self.id)
		
		
	def create_study_user(self, current_user):
		"""docstring for create_study_user"""
		StudyUser(study=self,user=current_user,role=1, group=Group.objects.filter(name="Investigator", study=self)).save()

	def users(self):
		"""docstring for users"""
		return [x.user for x in StudyUser.objects.filter(study=self)]

	def users_in_stage(self, stage):
		"""docstring for users"""
		return [x.user for x in StudyUser.objects.filter(current_stage=stage)]

	def getstudyuser(self, user):
		return StudyUser.objects.get(study=self, user=user)
	
	def number_users_in_stage(self, stage):
		"""docstring for number_users_in_stage"""
		return len(users_in_stage(stage))
			


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

#	def stages(self):
#		return [x.stage for x in StageGroup.objects.filter(group=self).order_by('order')]
		
class StudyUser(models.Model):
	study = models.ForeignKey(Study)
	user = models.ForeignKey(User)
	group = models.ForeignKey(Group)
	
	CHOICES = ((1, 'Investigator'),(0, 'Participant'))
	role = models.IntegerField("Role", max_length=1, choices=CHOICES)
	#current_condition = models.ForiengKey(Condition)
	
	current_stage = models.IntegerField('Current Stage', default=1)
	current_session = models.IntegerField('Current Session', default=1)
	last_action = models.DateTimeField('Last Session Completed')

	def stages(self):
		return [x.stage for x in StageGroup.objects.filter(group=self.group).order_by('order')]

	def totalstages(self):
		return StageGroup.objects.filter(group=self.group).count()
		
	def save(self):
		#create timestamps, keep track of user modifying, etc.
		print "saving..."
		super(StudyUser,self).save()
	
	def getcurrentstagenum(self):
		#get the current stage object
		currstage = StageGroup.objects.get(group=self.group, order=self.current_stage)
		return currstage.order
	def getcurrentstage(self):
		#get the current stage object
		currstage = StageGroup.objects.get(group=self.group, order=self.current_stage).stage
		return currstage
	def nextdeadline(self):
		ahead = datetime.timedelta(days=self.getcurrentstage().deadline)
		print self.last_action + ahead
		return self.last_action + ahead
		
	def overdue(self):
		if datetime.datetime.now() > self.deadline():
			return true
		return false
		
	def __unicode__(self):
		return u'%s - %s(%s)' % (self.user,self.study, self.role)		


		
class Stage(models.Model):
	name = models.CharField('Stage Name', max_length=300)
	study = models.ForeignKey(Study)
	sessions = models.IntegerField('Number of sessions')
	deadline = models.IntegerField('Time to finish session (in days)')
	url = models.URLField('Stage URL')
	description = tinymce_models.HTMLField('Stage Description')
	instructions = tinymce_models.HTMLField('Stage Instructions')

	def __unicode__(self):
		return unicode(self.name)		
	

	
class StageGroup(models.Model):
	group = models.ForeignKey(Group)
	stage = models.ForeignKey(Stage)
	order = models.IntegerField()

	def __unicode__(self):
		return u'%s - %s (%s)' % (self.stage, self.group, self.order)

