#Django
from django.db import models

#abstract cride.util
from cride.utils.models import CRideModel

class Circle(CRideModel):
    name=models.CharField("Circle name",max_length=140)
    slug_name=models.SlugField(unique=True,max_length=40)
    
    about=models.CharField("Circle description",max_length=255,blank=True)
    picture=models.ImageField(upload_to="circles/picture",blank=True,null=True)

    members=models.ManyToManyField("users.User",through="circles.Membership",through_fields=("circle","user"))

    rides_offered=models.PositiveIntegerField(default=0)
    rides_taken=models.PositiveIntegerField(default=0)

    verified=models.BooleanField(
        "Verified circle",
        default=False,
        help_text="Verified circle, only yes is official"
    )

    is_public=models.BooleanField(
        "Circle public",
        default=True
    )

    is_limit=models.BooleanField(
        "Limit of circle",
        default=False
    )
    members_limit=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        ordering=["-rides_taken","-rides_offered"]
