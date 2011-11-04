from django.contrib import admin
from portal.studies.models import *
from portal.users.models import UserProfile
import datetime

class StudyParticipantAdmin( admin.ModelAdmin ):
	{
	'fields': ('study', 'group','user'),
	}
	
	def save_model(self, request, obj, form, change):
		#get all stages for the group 
		for x in StageGroup.objects.filter(group=obj.group).order_by('order'):
			a = UserStage.objects.filter(user=obj.user, stage=x.stage)
			if x.order == 1 and len(a)<1:
				UserStage.objects.create(user=obj.user, stage=x.stage, study=obj.study, order=x.order, sessions_completed=0, status=1, start_date=datetime.datetime.now(), last_session_completed=datetime.datetime.now())
			elif len(a)<1:
				UserStage.objects.create(user=obj.user, stage=x.stage, study=obj.study, order=x.order, sessions_completed=0, status=2)
			else:
				pass
		obj.save()

# REMOVE USER_STAGE OBJECTS WHEN REMOVING STUDYPARTS

admin.site.register(Study)
admin.site.register(StudyParticipant, StudyParticipantAdmin)
admin.site.register(StudyInvestigator)
admin.site.register(Stage)
admin.site.register(UserStage)
admin.site.register(StageGroup)
admin.site.register(Group)
admin.site.register(Data)
admin.site.register(Alert)
admin.site.register(AlertRecepient)
admin.site.register(UserProfile)