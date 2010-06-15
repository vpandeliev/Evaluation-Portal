from django.db import models
from django.contrib.auth.models import User


class Study(models.Model):

	name = models.CharField('Study Name', max_length=300)
	description = models.CharField('Study Description', max_length=3000)
	start_date = models.DateField('Starting Date', blank=True, null=True)
	end_date = models.DateField('End Date', blank=True, null=True)
	started =  models.BooleanField('Started', default=False)
	
	def save(self, *args,**kwargs):
		#create timestamps, keep track of user
		#print "saving..."		
		super(Study, self).save(*args, **kwargs) 
		
	def create_study_user(self, current_user):
		"""docstring for create_study_user"""
		StudyUser(study=self,user=current_user,role=1).save()

	def users(self):
		"""docstring for users"""
		return [x.user for x in StudyUser.objects.filter(study=self)]
	
	def __unicode__(self):
		return u'%s - %s' % (self.name, self.start_date)
		
	# def __dict__(self):
	# 	"""docstring for __dict__"""
	# 	return {
	# 		'name': self.name,
	# 		'description': self.description,
	# 		'start_date': self.start_date,
	# 		'end_date': self.end_date,
	# 		'started': self.started,
	# 	}


class StudyUser(models.Model):
	study = models.ForeignKey(Study)
	user = models.ForeignKey(User)
	
	CHOICES = ((1, 'Investigator'),(0, 'Participant'))
	role = models.IntegerField("Role", max_length=1, choices=CHOICES)
	#current_condition = models.ForiengKey(Condition)
	deadline = models.DateTimeField('Deadline', blank=True, null=True)
	next_meeting = models.DateTimeField('Next Meeting', blank=True, null=True)


	def save(self):
		#create timestamps, keep track of user
		print "saving..."
		super(StudyUser,self).save()
		
		
	def __unicode__(self):
		return unicode(self.study.name)
		

# Create your models here.
