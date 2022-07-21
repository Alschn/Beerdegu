from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.utils import build_absolute_uri
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class UserPasswordResetForm(AllAuthPasswordResetForm):
    frontend_path = '/password/reset/confirm/{uid}/{token}/'

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = self.frontend_path.format(
                uid=user_pk_to_url_str(user),
                token=temp_key
            )

            if getattr(settings, 'REST_AUTH_PW_RESET_USE_SITES_DOMAIN', False) is True:
                url = build_absolute_uri(None, path)
            else:
                url = build_absolute_uri(request, path)

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)

            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )

        return self.cleaned_data['email']
