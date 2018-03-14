"""MetaGenScope custom renderers that wraps responses in envelope."""

from flask_api.renderers import JSONRenderer


class EnvelopeJSONRenderer(JSONRenderer):  # pylint: disable=too-few-public-methods
    """JSON Renderer that wraps response in enveloper {status, message, and data}."""

    media_type = 'application/json'

    def render(self, data, media_type, **options):
        """Wrap response in envelope."""
        response = {'status': 'error'}
        status_code = options['status_code']
        if status_code < 200 or status_code >= 300:
            detail = data['message']
            response['message'] = detail
        else:
            response['status'] = 'success'
            response['data'] = data
        return super(EnvelopeJSONRenderer, self).render(response, media_type, **options)
