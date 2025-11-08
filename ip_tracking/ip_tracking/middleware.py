from .models import RequestLog


class IPLoggingMiddleware:
    """
    Middleware to log the IP address, timestamp, and path of every incoming request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Get client IP address.
        HTTP_X_FORWARDED_FOR is the standard header for identifying the
        originating IP address of a client connecting to a web server
        through an HTTP proxy or a load balancer.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            # REMOTE_ADDR is the IP address of the client.
            ip_address = request.META.get('REMOTE_ADDR')

        # Log the request to the database
        if ip_address:
            RequestLog.objects.create(ip_address=ip_address, path=request.path)

        response = self.get_response(request)
        return response