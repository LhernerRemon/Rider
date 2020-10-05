#Django
from django.db import models

#abstract cride.util
from cride.utils.models import CRideModel

class Profile(CRideModel):
    user=models.OneToOneField("users.User",on_delete=models.CASCADE)
    picture=models.ImageField(
        "Profile picture",
        upload_to="user/pictures/",
        blank=True,
        null=True
    )
    biography=models.TextField(max_length=256,blank=True)

    #Stats
    rides_taken=models.PositiveIntegerField(default=0)
    rides_offered=models.PositiveIntegerField(default=0)
    reputation=models.FloatField(
        default=5.0,
        help_text="User's reputationbased  on the rides  taken on offered"
    )

    def __str__(self):
        return str(self.user)