#REST
from rest_framework.permissions import BasePermission

#Model
from cride.circles.models import Membership
class IsActiveCircleMember(BasePermission):
    
    def has_permission(self, request, view):
        try:
            Membership(user=request.user,circle=view.circle,is_activate=True)
        except Membership.DoesNotExist:
            return False
        return True

class IsSelfMember(BasePermission):

    def has_permission(self, request, view):
        obj=view.get_object()
        return super().has_object_permission(request, view,obj)
        
    def has_object_permission(self, request, view, obj):
        return request.user==obj.user