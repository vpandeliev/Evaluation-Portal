from models import *

def msgproc(request):
    "A context processor that provides access to a list of messages"
    print request.user
    if not request.user.is_anonymous():
        um = AlertRecepient.objects.filter(recepient=request.user, read='0')    
        unreadmsg = sorted(um, key=lambda n: (-(n.alert.date.year), -(n.alert.date.month), -(n.alert.date.day)))
        rm = AlertRecepient.objects.filter(recepient=request.user, read='1')
        readmsg = sorted(rm, key=lambda n: (-(n.alert.date.year), -(n.alert.date.month), -(n.alert.date.day)))
        alerts = Alert.objects.filter(author=request.user)
        studies = [x.study for x in StudyInvestigator.objects.filter(investigator=request.user)]    
        return {
        'unreadmsg': unreadmsg,
        'readmsg': readmsg,
        'alerts': alerts,
        'studies': studies, #use study.participants to get at list of participants
        }
    else:
        return {}
