#Django
from django.conf import settings
from django.contrib.auth import authenticate,password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

#REST
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

#User.models
from cride.users.models import User,Profile

#Utilities
import jwt
from datetime import timedelta
import datetime
import pytz
import time

from cride.users.serializers.profile import ProfileModelSerializer







class UserModelSerializer(serializers.ModelSerializer):#Para listar
	
	profile=ProfileModelSerializer(read_only=True)

	class Meta:
		model=User
		fields=(
			"username",
			"first_name",
			"last_name",
			"email",
			"phone_number",
			"profile"
		)



class UserLoginSerializer(serializers.Serializer):
	email=serializers.EmailField()
	password=serializers.CharField(min_length=8)

	def validate(self,data):
		user=authenticate(username=data["email"],password=data["password"])
		if not user:
			raise serializers.ValidationError("Invalid credentials")
		if not user.is_verfied:
			raise serializers.ValidationError("Account in not active yet :(")
		self.context["user"]=user
		return data

	def create(self,data):
		token,created=Token.objects.get_or_create(user=self.context["user"])
		return self.context["user"] , token.key




class UserSignupSerializer(serializers.Serializer):

	email=serializers.EmailField(
		validators=[UniqueValidator(queryset=User.objects.all())]
	)

	username=serializers.CharField(
		validators=[UniqueValidator(queryset=User.objects.all())],
		min_length=4,
		max_length=30
	)

	#Phone
	phone_regex=RegexValidator(regex=r'\+?1?\d{9,15}$',
		message="Phone number must be enteredin the  format +999999999. Up  to 15  digits allowed.")

	phone_number=serializers.CharField(validators=[phone_regex],required=False)

	password=serializers.CharField(max_length=64)
	password_confirmation=serializers.CharField(max_length=64)

	first_name=serializers.CharField(min_length=2,max_length=30)
	last_name=serializers.CharField(min_length=2,max_length=30)

	def validate(self,data):
		password=data.get("password")
		password_confirmation=data.get("password_confirmation")
		if password != password_confirmation:
			raise serializers.ValidationError("Passwords don't match.")
		password_validation.validate_password(password)
		return data

	def create(self,data): #.save()
		data.pop("password_confirmation")
		user=User.objects.create_user(**data,is_verfied=False,is_client=True)
		Profile.objects.create(user=user)
		self.send_confirmation_email(user)

		print("DATETIME--------------")
		print(datetime.datetime.now().strftime("%c"))
		print("TIME--------------")
		print(time.strftime("%c"))
		print("PYTZ--------------")
		print(pytz.timezone("America/Lima"))
		print("TIMEZONE--------------")
		print(timezone.now().strftime("%c"))
		print("--------------------------")
		print("Timezone plus 5 hours and 1/2")
		print(timezone.now()+timedelta(hours=5,minutes=30))


		return user

	def send_confirmation_email(self,user):
		verification_token=self.gen_verification_token(user)

		subject="Wellcome @{}! Verify your accountto start using CR".format(user.username)
		from_email="Comparte Ride <lherner21@gmail.com>"
		to=user.email
		content=render_to_string("emails/users/account_verification.html",
			{
				"token":verification_token,
				"user":user
			}
		)
		msg=EmailMultiAlternatives(subject,content,from_email,[to])
		msg.attach_alternative(content,"text/html")
		msg.send()



	def gen_verification_token(self,user):
		exp_date=timezone.now()+timedelta(days=3)
		payload={
			"user":user.username,
			"exp":int(exp_date.timestamp()),
			"type":"Email confirmation"
		}
		token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
		return token.decode()

class AccountVerificationSerializer(serializers.Serializer):
	token=serializers.CharField()
	
	def validate_token(self,data):
		try:
			payload=jwt.decode(data,settings.SECRET_KEY,algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			raise serializers.ValidationError("Verification  link has expired")
		except jwt.PyJWTError:
			raise serializers.ValidationError("Invalid token")
		if payload["type"] != "Email confirmation":
			raise serializers.ValidationError("Invalid token, type.")
		self.context["payload"]=payload
		return data

	def save(self):
		payload=self.context["payload"]
		user=User.objects.get(username=payload["user"])
		user.is_verfied=True
		user.save()