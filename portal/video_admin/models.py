"""
    Extending the django auth User model to have a flag that specifies whether or
    not they have a video conference invitation
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    has_pending_request = models.IntegerField()
    user = models.ForeignKey(User, unique=True)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile(user=user, has_pending_request=0)
        profile.save()


# register signal handler
post_save.connect(create_profile, sender=User, dispatch_uid="users-profilecreation-signal")
