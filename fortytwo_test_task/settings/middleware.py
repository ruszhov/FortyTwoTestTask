from django.conf import settings
from apps.hello.models import HttpRequestLog
from datetime import datetime


class HttpLoggingRequestMiddleware(object):
    """
    Middleware that stores http requests in DB
    """

    def process_request(self, request):
        if getattr(settings, 'ENABLE_HTTP_REQUEST_LOGGING'):
            log = HttpRequestLog(
                            date=datetime.now(),
                            request_method=request.META.get(
                                'REQUEST_METHOD', '?'),
                            url=request.path[:256],
                            server_protocol=request.META.get(
                                'SERVER_PROTOCOL', '?')
                        )
            log.save()
        pass
