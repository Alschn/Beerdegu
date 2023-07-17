from allauth.account.adapter import DefaultAccountAdapter

from core.shared.frontend import get_frontend_domain


def build_frontend_url(path: str) -> str:
    domain = get_frontend_domain()
    return domain + path


class AccountAdapter(DefaultAccountAdapter):
    password_reset_url_path = '/auth/password/reset/confirm/?uid={uid}&token={token}'
    email_confirmation_url_path = '/auth/register/confirm/?key={key}'

    def get_email_confirmation_url(self, request, emailconfirmation) -> str:
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """

        key = emailconfirmation.key
        frontend_path = self.email_confirmation_url_path.format(key=key)
        return build_frontend_url(frontend_path)

    def get_password_reset_url(self, request, uid: str, token: str) -> str:
        """Constructs the password reset url."""

        frontend_path = self.password_reset_url_path.format(uid=uid, token=token)
        return build_frontend_url(frontend_path)
