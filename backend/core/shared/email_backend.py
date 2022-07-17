from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.utils.module_loading import import_string
from django_q.tasks import async_task

DEFAULT_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = getattr(settings, 'DJANGO_Q_EMAIL_BACKEND', DEFAULT_BACKEND)
EMAIL_ERROR_HANDLER = getattr(settings, 'DJANGO_Q_EMAIL_ERROR_HANDLER', None)
DJANGO_Q_EMAIL_USE_DICTS = getattr(settings, 'DJANGO_Q_EMAIL_USE_DICTS', True)


class DjangoQBackend(BaseEmailBackend):
    use_dicts = DJANGO_Q_EMAIL_USE_DICTS

    def send_messages(self, email_messages):
        num_sent = 0
        for email_message in email_messages:
            if self.use_dicts:
                email_message = to_dict(email_message)
            async_task('core.shared.email_backend.send_message', email_message)
            num_sent += 1
        return num_sent


def send_message(email_message):
    """
    Sends the specified email synchronously.
    See DjangoQBackend for sending in the background.
    """
    try:
        if isinstance(email_message, dict):
            email_message = from_dict(email_message)
        connection = email_message.connection
        email_message.connection = get_connection(backend=EMAIL_BACKEND)
        try:
            email_message.send()
        finally:
            email_message.connection = connection
    except Exception as ex:
        if not EMAIL_ERROR_HANDLER:
            raise
        email_error_handler = import_string(EMAIL_ERROR_HANDLER)
        email_error_handler(email_message, ex)


def to_dict(email_message):
    """
    Converts the specified email message to a dictionary representation.
    """
    if type(email_message) not in [EmailMessage, EmailMultiAlternatives]:
        return email_message

    email_message_data = {
        'subject': email_message.subject,
        'body': email_message.body,
        'from_email': email_message.from_email,
        'to': email_message.to,
        'bcc': email_message.bcc,
        'attachments': email_message.attachments,
        'headers': email_message.extra_headers,
        'cc': None,
        'reply_to': None,
    }

    if isinstance(email_message, EmailMultiAlternatives):
        email_message_data['alternatives'] = email_message.alternatives

    return email_message_data


def from_dict(email_message_data):
    """
    Creates an EmailMessage or EmailMultiAlternatives instance from the
    specified dictionary.
    """
    kwargs = dict(email_message_data)
    alternatives = kwargs.pop('alternatives', None)
    return (
        EmailMessage(**kwargs) if not alternatives else
        EmailMultiAlternatives(alternatives=alternatives, **kwargs)
    )
