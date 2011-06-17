# for modifying the new profile in the admin interface
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from portal.video_admin.models import UserProfile


# unregister old user admin
admin.site.unregister(User)


class UserProfileInline(admin.TabularInline):
     model = UserProfile
     fk_name = 'user'
     max_num = 1
     can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]
    list_display = ('username', 'first_name', 'last_name', 'has_pending_request', 'is_staff')

    def has_pending_request(self, instance):
        # instance is User instance
        return instance.get_profile().has_pending_request
            
# register new user admin
admin.site.register(User, UserProfileAdmin)
