import logging
from django.utils import timezone
from django.conf import settings
from customModels.models import RequestLogger

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before it reaches the view
        response = self.get_response(request)

        # Log the request
        self.log_request(request)

        return response

    def log_request(self, request): 
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Use timezone-aware datetime
            current_hour = timezone.now().replace(minute=0, second=0, microsecond=0)

            # Get or create a log entry for the user and current hour
            log_entry, created = RequestLogger.objects.get_or_create(
                user=request.user,
                hour=current_hour,
            )

            # Increment the request count
            log_entry.request_count += 1
            log_entry.save()

            # Optionally, log to console or file for debugging
            if settings.DEBUG:
                print(f"User {request.user} request to {request.path}. Total rq/h: {log_entry.request_count}")
