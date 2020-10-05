#REST
from rest_framework import serializers

#Django
from django.utils import timezone

#models
from cride.circles.models import Membership,Circle,Invitation

#Seralizer
from cride.users.serializers import UserModelSerializer

class MembershipModelSerializer(serializers.ModelSerializer):

    joined_at=serializers.DateTimeField(source="created",read_only=True)
    invited_by=serializers.StringRelatedField()
    user=UserModelSerializer(read_only=True)
    #read_only...no pide esto como campo
    #source....campo a hacer referencia
    class Meta:
        model=Membership
        fields=(
            "user",
            "is_admin",
            "is_activate",
            "user_invitations",
            "remaining_invitation",
            "invited_by",
            "rides_taken","rides_offered",
            "joined_at"
        )
        read_only_fields=("rides_taken","rides_offered","user","invited_by")

class AddMemberSerializer(serializers.Serializer):

    invitation_code=serializers.CharField(min_length=8)
    user=serializers.HiddenField(default=serializers.CurrentUserDefault)#

    def validate_user(self,data):
        circle=self.context["circle"]
        user=data
        q=Membership.objects.filter(circle=circle,user=user)
        if q.exists():
            raise serializers.ValidationError("User is already member of the circle")
    
    def validate_invitation_code(self,data):
        try:
            invitation=Invitation.objects.get(code=data,circle=self.context["circle"],used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid invitation code")
        self.context["invitation"]=invitation
        return data

    def validate(self,data):
        circle=self.context["circle"]
        if circle.is_limited and circle.members.count()>=circle.members_limit:
            raise serializers.ValidationError("Circle has reached  it's member limit")
        return data
    
    def create(self,data):
        circle=self.context["circle"]
        invitation=self.context["invitation"]
        user=data["user"]
        now=timezone.now()

        member=Membership.objects.create(user=user,profile=user.profile,circle=circle,invited_by=invitation.issued_by)

        invitation.used_by=user
        invitation.used=True
        invitation.used_at=now
        invitation.save()

        issuer=Membership.objects.get(user=invitation.issued_by,circle=circle)
        issuer.used_invitation+=1
        issuer.remaining_invitation-=1
        issuer.save()

        return member