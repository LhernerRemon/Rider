#REST
from rest_framework.permissions import BasePermission

#Members
from cride.circles.models import Membership

class IsCircleAdmin(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_activate=True
            )
        except Membership.DoesNotExist:
            return False
        return True
