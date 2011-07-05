# we can put anything we want here. This can read all the directories in here
# and do some setup???

# This file must create the urls.py and views.py appropriately for each study.
#   For a given study we need:
#       urls.py:
#           one 
#
import os, sys

from user_studies.study_builder import *
from django.core.exceptions import MiddlewareNotUsed


class FileBuilderMiddleware:
    def process_request(self, request):
        pass
    
    
    def __init__(self):
        # Get the names of all the study folders in this directory
        module_dir = os.path.dirname(__file__) + "/user_studies"
        files = ["{0}/{1}".format(module_dir, f) for f in os.listdir(module_dir)]
        study_dirs = [f for f in files if os.path.isdir(f) and f.find("study_builder") == -1]
        
        # parse and save the settings files for each study
        all_settings = []
        for directory in study_dirs:
            all_settings.append(get_study_settings(directory))
        
        # generate a sample views.py file to see if this approach will work
        views_file = open("{0}/{1}".format(module_dir, "views.py"), "w")
        views_builder = ViewsBuilder(*all_settings)
        views_builder.write_views_file(views_file)
        
        
        # generate a sample urls.py file to see if this approach will work
        urls_file = open("{0}/{1}".format(module_dir, "urls.py"), "w")
        urls_builder = UrlsBuilder(*all_settings)
        urls_builder.write_urls_file(urls_file)
    
        raise MiddlewareNotUsed



