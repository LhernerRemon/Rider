#Django
from django.db import models

#Utilities
from cride.utils.models import CRideModel

#Manager
from cride.circles.managers import InvitationManager

class Invitation(CRideModel):

    code=models.CharField(max_length=50,unique=True)

    issued_by=models.ForeignKey("users.User",on_delete=models.CASCADE,null=True,related_name="issued_by")

    used_by=models.ForeignKey("users.User",on_delete=models.CASCADE,null=True,help_text="Usuario que usó el código para ingresar al círculo")

    circle=models.ForeignKey("circles.Circle",on_delete=models.CASCADE)

    used=models.BooleanField(default=False,help_text="Invitación usada?")

    used_at=models.DateTimeField(blank=True,null=True,help_text="Fecha de uso")

    objects=InvitationManager()

    def __str__(self):
        return "{}: {}".format(self.circle.slug_name,self.code)