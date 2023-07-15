from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str, user_username
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class UserPasswordResetForm(AllAuthPasswordResetForm):

    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        adapter = get_adapter(request)
        assert hasattr(adapter, 'get_password_reset_url'), 'get_password_reset_url() must be implemented in Adapter'

        for user in self.users:
            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            url = adapter.get_password_reset_url(
                request,
                uid=user_pk_to_url_str(user),
                token=temp_key
            )

            context = {
                'current_site': settings.FRONTEND_SITE_NAME,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)

            adapter.send_mail(
                'account/email/password_reset_key', email, context
            )

        return self.cleaned_data['email']
