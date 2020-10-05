#Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#abstract cride.util
from cride.utils.models import CRideModel

class User(CRideModel,AbstractUser):
    email=models.EmailField(
        "Email adress",
        unique=True,
        error_messages={
            "unique":"A user with  that email already exist."
        }
    )

    phone_regex=RegexValidator(regex=r'\+?1?\d{9,15}$',
    message="Phone number must be enteredin the  format +999999999. Up  to 15  digits allowed.")
    phone_number=models.CharField(validators=[phone_regex],max_length=17,blank=True)

    USERNAME_FIELD="email"

    REQUIRED_FIELDS=["username","first_name","last_name"]

    is_client=models.BooleanField(
        "Client status",
        default=True,
        help_text="help easily distinguish user"
    )

    is_verfied=models.BooleanField(
        "Verified",
        default=False,
        help_text="Set to true  when the user have verified its email adress"
    )

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username
