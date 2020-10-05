#REST
from rest_framework import serializers

#Model
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):

    members_limit=serializers.IntegerField(
       required=False,
       min_value=10,
       max_value=32000
    )
    is_limit=serializers.BooleanField(default=False)


    class Meta:
        model=Circle
        fields=("name","slug_name","about","picture","rides_offered","rides_taken","verified","is_public","is_limit","members_limit")
        read_only_fields=("is_public","verified","rides_offered","rides_taken")#Datos que no se pueden cambiar

    def validate(self, data):
        members_limit=data.get("members_limit",None)
        is_limit=data.get("is_limit",False)

        if is_limit ^ bool(members_limit):
            raise serializers.ValidationError("If circle is limited.")
        return data