# we can put anything we want here. This can read all the directories in here
# and do some setup???

# This file must create the urls.py and views.py appropriately for each study.
#   For a given study we need:
#       urls.py:
#           one 
#
#
#   TODO:
#       Don't do this each time the server starts up. Create a separate page for
#       building studies (with some user interaction) that makes it clear what
#       is happening at each step, and does some error checking
#
#       This is OK for now, while I clean up the code... we can ensure that 
#       everyting is being generated appropriately as I delete piles of stuff


import os, sys

from django.core.exceptions import MiddlewareNotUsed
from django.contrib.auth.models import User

from studies.models import Study, Group, Stage, StageGroup, StudyParticipant, UserStage
from user_studies.study_builder import *


class FileBuilderMiddleware:
    def process_request(self, request):
        pass
    
    
    def create_study_urls_and_views(self):
        """
            Generates user_studies/urls.py and user_studies/views.py based on the
            settings objects contained in self.settings_list
        """
        # generate a sample views.py file to see if this approach will work
        views_builder = ViewsBuilder(*self.all_settings)
        views_builder.write_views_file(self.module_dir)

        # generate a sample urls.py file to see if this approach will work
        urls_builder = UrlsBuilder(*self.all_settings)
        urls_builder.write_urls_file(self.module_dir)
    
    
    def create_participants(self):
        """
            Create user entries in the database for each study in 
            self.settings_list.
            
            This will override any existing users password with the one that is
            supplied in settings.xml
        """
        for s in self.all_settings:
            for username in s.participants:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username)
                
                # TODO: read this in from the .xml file
                user.set_password("default")
                user.save()
    
    
    def create_studies(self):
        """
            Create Study entries in the database for each study in 
            self.settings_list.
        """
        for s in self.all_settings:
            try:
                study = Study.objects.get(name=s.name)
            except Study.DoesNotExist:
                study = Study(name=s.name)
            
            study.stub = s.name_stub
            study.description = s.description
            #study.start_date = Date
            #study.end_date = Date
            study.started = True
            study.consent = s.informed_consent
            study.instructions = s.instructions
            study.eligibility = s.eligibility
            study.reward = s.reward
            study.task_session_dur = 1
            study.assess_blocks = 1
            study.assess_trials = 1
            
            study.save()
      
    
    def create_group(self, study, group_name):
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            group = Group(name=group_name)
    
        group.study = study
        group.save()
        
        return group
    
    
    def create_groups(self):
        """
            Create Group entries in the database for each study in 
            self.settings_list.
            
            TODO: Warn user if a group already exists under another study
        """
        for s in self.all_settings:
            # create_studies was called before this so we should have the study
            # object in the database
            study = Study.objects.get(name=s.name)
            for group_name in s.groups.keys():
                users = s.groups[group_name]['users']
                stages = s.groups[group_name]['stages']
                
                group = self.create_group(study, group_name)
                
                # specify the order that the stages appear for this group
                stage_index = 0
                for stage_name in stages:
                    stage = Stage.objects.get(name=stage_name)
                    try:
                        stage_group = StageGroup.objects.get(group=group, stage=stage, order=stage_index)
                    except StageGroup.DoesNotExist:
                        stage_group = StageGroup(group=group, stage=stage, order=stage_index)
                    stage_group.save()
                
                    
                    # add study participants for the group
                    for username in users:
                        user = User.objects.get(username=username)
                        try:
                            study_participant = StudyParticipant.objects.get(study=study, user=user, group=group)
                        except StudyParticipant.DoesNotExist:
                            study_participant = StudyParticipant(study=study, user=user, group=group)
                        study_participant.save()
                        
                        # add a UserStage for each user/stage pair
                        try:
                            user_stage = UserStage.objects.get(stage=stage, user=user, order=stage_index, study=study)
                        except UserStage.DoesNotExist:
                            user_stage = UserStage(stage=stage, user=user, order=stage_index, study=study)  
                        # set all status to incomplete
                        user_stage.status = 1 if stage_index == 0 else 2
                        user_stage.sessions_completed = 0
                        user_stage.save()
                        
                    stage_index = stage_index + 1
                    
    
    
    def create_stages(self):
        """
        Create Stage entries in the database for each study in 
        self.settings_list.
        """
        for s in self.all_settings:
            study = Study.objects.get(name=s.name)
            for stage_name in s.stages:
                try:
                    stage = Stage.objects.get(name=stage_name)
                except Stage.DoesNotExist:
                    stage = Stage(name=stage_name)
                stage.stub = stage_name[0:3]
                stage.study = study
                stage.sessions = 1
                stage.deadline = 10
                
                stage.url = "/user_studies/{0}/{1}".format(study.name, stage.name)
                 
                stage.description = "Stage description goes here :P"
                stage.instructions = "Stage instructions go here :D"
                
                stage.save()
        
    
    def __init__(self):
        # Get the names of all the study folders in the user studies directory
        self.module_dir = os.path.dirname(__file__) + "/user_studies"
        self.files = ["{0}/{1}".format(self.module_dir, f) for f in os.listdir(self.module_dir)]
        self.study_dirs = [f for f in self.files if os.path.isdir(f) and f.find("study_builder") == -1]
        
        # parse and save the settings files for each study
        self.all_settings = []
        for directory in self.study_dirs:
            self.all_settings.append(StudySettings(directory))
        
        print self.all_settings[0]
        self.create_study_urls_and_views()
        self.create_studies()
        self.create_participants()
        self.create_stages()
        self.create_groups()
        
        raise MiddlewareNotUsed



