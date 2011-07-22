# we can put anything we want here. This can read all the directories in here
# and do some setup???

# This file must create the urls.py and views.py appropriately for each study.
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

from study_builder import *


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
    
    
    def __init__(self):
        # Get the names of all the study folders in the user studies directory
        self.module_dir = os.path.dirname(__file__) + "/user_studies"
        self.files = ["{0}/{1}".format(self.module_dir, f) for f in os.listdir(self.module_dir)]
        self.study_dirs = [f for f in self.files if os.path.isdir(f) and f.find("study_builder") == -1]
        
        # parse and save the settings files for each study
        self.all_settings = []
        for directory in self.study_dirs:
            self.all_settings.append(StudySettings(directory))
        
        self.create_study_urls_and_views()
        
        raise MiddlewareNotUsed



