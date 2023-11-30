from django.conf import settings
from rest_framework.permissions import BasePermission


class IsInternalServicePermission(BasePermission):
    def has_permission(self, request, view):
        service_internal_id = request.headers.get(settings.INTERNAL_SERVICES_AUTH_HEADER)
        return service_internal_id in settings.ALLOWED_INTERNAL_SERVICES_IDS
