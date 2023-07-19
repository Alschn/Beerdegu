from typing import Any

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import user_pk_to_url_str, user_username
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str

from core.shared.frontend import get_frontend_site, build_frontend_url

EmailConfirmationType = EmailConfirmation | EmailConfirmationHMAC

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):
    # paths
    email_confirmation_url_path = '/auth/register/confirm/?key={key}'
    password_reset_url_path = '/auth/password/reset/confirm/?uid={uid}&token={token}'

    # templates
    email_confirmation_signup_template = "account/email/email_confirmation_signup"
    email_confirmation_template = "account/email/email_confirmation"
    password_reset_template = "account/email/password_reset_key"

    def send_confirmation_mail(
        self, request: Any, emailconfirmation: EmailConfirmationType, signup: bool
    ) -> None:
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        frontend_site = get_frontend_site()
        ctx = {
            "current_site": frontend_site,
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = self.email_confirmation_signup_template
        else:
            email_template = self.email_confirmation_template

        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def send_password_reset_mail(
        self, request: Any, email: str, user: User, token_generator: PasswordResetTokenGenerator
    ) -> None:
        """
        Sends an email with a link to password reset page.
        Password reset email logic based on AllAuthPasswordResetForm.save()
        """

        temp_key = token_generator.make_token(user)

        # (optionally) save it to the password reset model
        # password_reset = PasswordReset(user=user, temp_key=temp_key)
        # password_reset.save()

        uid = user_pk_to_url_str(user)
        url = self.get_password_reset_url(request, uid, temp_key)

        frontend_site = get_frontend_site()
        context = {
            'current_site': frontend_site,
            'user': user,
            'password_reset_url': url,
            'request': request,
        }
        if allauth_settings.AUTHENTICATION_METHOD != allauth_settings.AuthenticationMethod.EMAIL:
            context['username'] = user_username(user)

        self.send_mail(self.password_reset_template, email, context)

    def get_email_confirmation_url(
        self, request: Any, emailconfirmation: EmailConfirmationType
    ) -> str:
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """

        key = emailconfirmation.key
        frontend_path = self.email_confirmation_url_path.format(key=key)
        return build_frontend_url(frontend_path)

    def get_password_reset_url(
        self, request: Any, uid: str, token: str
    ) -> str:
        """Constructs the password reset url."""

        frontend_path = self.password_reset_url_path.format(uid=uid, token=token)
        return build_frontend_url(frontend_path)

    def format_email_subject(self, subject: str) -> str:
        prefix = allauth_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site = get_frontend_site()
            prefix = "[{name}] ".format(name=site.name)
        return prefix + force_str(subject)
