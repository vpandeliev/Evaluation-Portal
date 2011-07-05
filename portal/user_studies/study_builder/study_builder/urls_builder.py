"""
    Classes and functions for generating urls.py files 
"""
from study_settings import StudySettings

#url_args = [("") for s in generated_studies]
#patterns_args = map(url, *x for x in url_args)
#urlpatterns = patterns(*patterns_args)



class UrlsBuilder:
    """
        Class for creating urls.py files from StudySettings objects.
    """
    
    urls_file_template = r"""
from django.conf.urls.defaults import *
from portal.user_studies.views import *

urlpatterns = patterns('', {0})
    """
    #url(r'^study_dir/stage_one$', stage_one, name="stage_one"),
    stage_url_template = "url(r'^{0}/{1}$', {1}, name='{1}')"
    
    def __init__(self, *settings_list):
        self.settings_list = settings_list
       
    def write_urls_file(self, file):
        url_list = []
        for study in self.settings_list:
            for stage in study.stages:
                url_list.append(UrlsBuilder.stage_url_template.format(study.name, stage))
        
        file.write(UrlsBuilder.urls_file_template.format(", ".join(url_list)))