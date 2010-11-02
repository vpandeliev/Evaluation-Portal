from django import forms
from portal.studies.models import *
from django.contrib.admin import widgets
	
class NewStudyForm(forms.ModelForm):
    class Meta:
        model = Study
    def __init__(self, *args, **kwargs):
        super(NewStudyForm, self).__init__(*args, **kwargs)

class AddParticipantForm(forms.Form):
    email = forms.EmailField()
    role = forms.BooleanField(label="Investigator?", required=False) #participant by default

class QForm(forms.Form):
    MCUNIQUE =  (('a', 'Answer a'),('b', 'Answer b'))
    MCNONUNIQUE = (('fruit', 'Fruits'),('veg', 'Veggies'))
    MCSCALE = ((1,"1 (Not at all)"),
                (2,"2"),
                (3,"3"),
                (4,"4 (Somewhat)"),
                (5,"5"),
                (6,"6"),
                (7,"7 (Totally)"))
    
    shortanswer = forms.CharField(label="How often do you eat salad?",max_length=100,widget=forms.TextInput)
    longanswer = forms.CharField(label="Tell us about your most memorable childhood experience.",widget=forms.Textarea)
    multiple_unique = forms.ChoiceField(widget=forms.RadioSelect, choices=MCUNIQUE)
    multiple_nonunique = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MCNONUNIQUE)
    multiple_scale = forms.ChoiceField(widget=forms.RadioSelect, choices=MCSCALE)
    
    
    
