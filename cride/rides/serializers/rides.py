#REST
from rest_framework import serializers

# Model
from cride.rides.models import Ride

class CreateRideSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Ride
        exclude=("offered_in","passengers","rating","is_active")

