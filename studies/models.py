from django.db import models
from django.contrib.auth.models import User


class Study(models.Model):

	name = models.CharField('Study Name', max_length=300)
	description = models.CharField('Study Description', max_length=3000)
	start_date = models.DateTimeField('Starting Date')
	end_date = models.DateTimeField('End Date')
	started =  models.BooleanField('Started')
	
	def save(self):
		#create timestamps, keep track of user
		print "saving..."
		super(Study,self).save()
		
	def users(self):
		"""docstring for users"""
		return [x.user for x in StudyUser.objects.filter(study=self)]
	
	def __unicode__(self):
		return u'%s - %s' % (self.name, self.start_date)


class StudyUser(models.Model):
	study = models.ForeignKey(Study)
	user = models.ForeignKey(User)
	
	CHOICES = ((1, 'Investigator'),(0, 'Participant'))
	role = models.IntegerField("Role", max_length=1, choices=CHOICES)
	#current_condition = models.ForiengKey(Condition)
	deadline = models.DateTimeField('Deadline')
	next_meeting = models.DateTimeField('Next Meeting')


	def save(self):
		#create timestamps, keep track of user
		print "saving..."
		super(StudyUser,self).save()
		
		
	def __unicode__(self):
		return unicode(self.study.name)
		

# Create your models here.
