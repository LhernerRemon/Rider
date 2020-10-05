#REST
from rest_framework import mixins,viewsets
from rest_framework.generics import get_object_or_404

#REST permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsActiveCircleMember

#Serializer
from cride.rides.serializers import CreateRideSerializer

#Model
from cride.circles.models import Circle
from 

class RideViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):

    serializer_class=CreateRideSerializer
    permissions_clasess=[IsAuthenticated,IsActiveCircleMember]

    def dispatch(self, request, *args, **kwargs):
        slug_name=kwargs["slug_name"]
        self.circle=get_object_or_404(Circle,slug_name=slug_name)
    
        return super(RideViewSet,self).dispatch(request,*args,**kwargs)