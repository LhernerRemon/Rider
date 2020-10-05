#Django
from django.db import models

#Utilities
from cride.utils.models import CRideModel

class Membership(CRideModel):

    user=models.ForeignKey("users.User",on_delete=models.CASCADE)
    profile=models.ForeignKey("users.Profile",on_delete=models.CASCADE)
    circle=models.ForeignKey("circles.Circle",on_delete=models.CASCADE)

    is_admin=models.BooleanField("Circle admin",default=False,help_text="If is admin of the circle")

    #Invitation
    user_invitations=models.PositiveIntegerField(default=0,help_text="Invitaciones usadas")
    remaining_invitation=models.PositiveIntegerField(default=0,help_text="Invitaciones que te quedan")
    invited_by=models.ForeignKey("users.User",null=True,on_delete=models.SET_NULL,related_name="invited_by")

    #Stats
    rides_taken=models.PositiveIntegerField(default=0)
    rides_offered=models.PositiveIntegerField(default=0)

    #Status
    is_activate=models.BooleanField("Active status",default=True)


    def __str__(self):
        return "@{} to #{}".format(self.user.username,self.circle.slug_name)