from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from dj_rest_auth.forms import AllAuthPasswordResetForm


class UserPasswordResetForm(AllAuthPasswordResetForm):

    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        adapter = get_adapter(request)
        assert (
            hasattr(adapter, 'send_password_reset_mail'),
            'send_password_reset_mail(request, email, user, token_generator) must be implemented in Adapter'
        )

        for user in self.users:
            adapter.send_password_reset_mail(request, email, user, token_generator)

        return self.cleaned_data['email']
