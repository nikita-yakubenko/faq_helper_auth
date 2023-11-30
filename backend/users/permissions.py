from rest_framework import permissions

from users.models import Organization


class IsOrganizationOwner(permissions.BasePermission):
    message = 'Access for this organization is restricted for you.'

    def has_permission(self, request, view):
        try:
            org = request.user.organization_set.get(id=view.kwargs.get('org_id', None))
            return True
        except Organization.DoesNotExist:
            return False