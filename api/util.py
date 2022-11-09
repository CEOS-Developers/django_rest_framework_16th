from rest_framework.renderers import JSONRenderer
from .common import *


# response customizing
class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = renderer_context.get('response')

        response = custom_response(response_data.status_code, data)

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
