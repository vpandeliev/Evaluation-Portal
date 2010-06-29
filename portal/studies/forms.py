from django import forms
from portal.studies.models import Study
from django.contrib.admin import widgets
	
class NewStudyForm(forms.ModelForm):
    class Meta:
        model = Study
    def __init__(self, *args, **kwargs):
        super(NewStudyForm, self).__init__(*args, **kwargs)

class AddParticipantForm(forms.Form):
    email = forms.EmailField()
    role = forms.BooleanField(label="Investigator?", required=False) #participant by default
