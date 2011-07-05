"""
    Classes and functions for generating views.py files for simple studies
"""
from study_settings import StudySettings

#url_args = [("") for s in generated_studies]
#patterns_args = map(url, *x for x in url_args)
#urlpatterns = patterns(*patterns_args)





class ViewsBuilder:
    """
        Class for creating urls.py files from StudySettings objects.
    """
    
    views_file_template = r"""
from django.http import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

{0}
"""
    
    #@login_required
    #def stage_two(request):
    #    return render_to_response('tutorial_study/study_display.html', {'number': 2})
    stage_url_template = """
@login_required
def {1}(request):
    return render_to_response('{0}/{1}.html')
"""
    
    def __init__(self, *settings_list):
        self.settings_list = settings_list
      
    def write_views_file(self, file):
        fcn_list = []
        for study in self.settings_list:
            for stage in study.stages:
                
                fcn_list.append(ViewsBuilder.stage_url_template.format(study.name, stage))
        file.write(ViewsBuilder.views_file_template.format("\n".join(fcn_list)))







