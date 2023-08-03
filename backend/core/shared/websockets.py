import re
from typing import Any
from urllib.parse import ParseResult

from channels.security.websocket import OriginValidator


class RegexOriginValidator(OriginValidator):

    def __init__(self, application, allowed_origins, regex_allowed_origins):
        self.regex_allowed_origins = regex_allowed_origins
        super().__init__(application, allowed_origins)

    def valid_origin(self, parsed_origin: ParseResult) -> bool:
        is_valid_origin = super().valid_origin(parsed_origin)
        return is_valid_origin or self.valid_regex_origin(parsed_origin)

    def valid_regex_origin(self, parsed_origin: ParseResult) -> bool:
        origin_to_string = parsed_origin.geturl()

        for origin_pattern in self.regex_allowed_origins:
            try:
                pattern = re.compile(origin_pattern)
            except re.error:
                continue

            match = pattern.match(origin_to_string)
            if match:
                return True

        return False


def CORSAllowedOriginValidator(application: Any) -> RegexOriginValidator:
    """
    Allowed hosts origin validator for Django Channels, which handles
    `ALLOWED_HOSTS`, `CORS_ORIGIN_WHITELIST` and `CORS_ORIGIN_REGEX_WHITELIST` settings.

    Required if frontend is hosted on a different domain than the backend.
    """
    from django.conf import settings

    allowed_hosts = settings.ALLOWED_HOSTS
    cors_origin_whitelist = getattr(settings, 'CORS_ORIGIN_WHITELIST', [])
    cors_origin_regex_whitelist = getattr(settings, 'CORS_ORIGIN_REGEX_WHITELIST', [])

    allowed_origins = {*allowed_hosts, *cors_origin_whitelist}
    regex_allowed_origins = {*cors_origin_regex_whitelist}

    return RegexOriginValidator(application, allowed_origins, regex_allowed_origins)
