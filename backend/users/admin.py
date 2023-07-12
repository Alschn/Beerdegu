from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportActionModelAdmin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin as BaseOutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

User = get_user_model()


class UserAdmin(ImportExportActionModelAdmin, BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')


class OutstandingTokenAdmin(BaseOutstandingTokenAdmin):
    """Overrides simple_jwt's token admin, so that deleting users is possible."""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return True


# unregister unnecessary models
admin.site.unregister([Group])

# register user with new user admin
admin.site.register(User, UserAdmin)

# unregister model and later register it with a new admin
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
