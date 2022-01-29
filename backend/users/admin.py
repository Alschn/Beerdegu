from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from import_export.admin import ImportExportActionModelAdmin

User = get_user_model()


class UserAdmin(ImportExportActionModelAdmin, BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


# unregister unnecessary models
admin.site.unregister([EmailAddress, Group, Site, SocialApp, SocialAccount, SocialToken])

# register user with new user admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
