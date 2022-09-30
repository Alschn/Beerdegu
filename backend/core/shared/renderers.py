from typing import Any

from rest_framework import status, renderers


class FileOrJSONRenderer(renderers.JSONRenderer):

    def render(
        self, data: Any, accepted_media_type: str | None = None, renderer_context: dict = None
    ) -> Any:
        if (response := renderer_context.get('response')) and response.status_code != status.HTTP_200_OK:
            return super().render(data, accepted_media_type, renderer_context)
        return data
