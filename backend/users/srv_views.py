import json

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from backend.permissions import IsInternalServicePermission
from users.models import User


@api_view(['GET'])
@permission_classes([IsInternalServicePermission])
def get_user_organizations(request, pk):
    user = get_object_or_404(User.objects.all(), pk=pk)
    data = [org.id for org in user.organization_set.all()]
    return Response({"data": json.dumps(data)})
