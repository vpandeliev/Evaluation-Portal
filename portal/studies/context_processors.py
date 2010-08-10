from models import *

def msgproc(request):
    "A context processor that provides access to a list of messages"
    um = AlertRecepient.objects.filter(recepient=request.user, read='0')
    unreadmsg = sorted(um, key=lambda n: (-(n.alert.date.year), -(n.alert.date.month), -(n.alert.date.day)))
    rm = AlertRecepient.objects.filter(recepient=request.user, read='1')
    readmsg = sorted(rm, key=lambda n: (-(n.alert.date.year), -(n.alert.date.month), -(n.alert.date.day)))

    return {
    'unreadmsg': unreadmsg,
    'readmsg': readmsg,
    
    }
