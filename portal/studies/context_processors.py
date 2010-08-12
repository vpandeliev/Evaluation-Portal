from models import *

def msgproc(request):
    "A context processor that provides access to a list of messages"
    um = AlertRecepient.objects.filter(recepient=request.user, read='0')
    unreadmsg = sorted(um, key=lambda n: (-(n.alert.date.year), -(n.alert.date.month), -(n.alert.date.day)))
    rm = AlertRecepient.objects.filter(recepient=request.user, read='1')
    readmsg = sorted(rm, key=lambda n: (-(n.alert.date.year), -(n.alert.date.month), -(n.alert.date.day)))

    alerts = []
    alert_recepients = Alert.objects.filter(author=request.user)
    for x in alerts:
        alerts.append([a.recepient.username for a in AlertRecepient.objects.filter(alert=x)])
        
    return {
    'unreadmsg': unreadmsg,
    'readmsg': readmsg,
    'alerts': alerts, #messages
    'alert_recepients': alert_recepients #recepient for each message above
    }
