#Django
from django.urls import path,include

#REST
from rest_framework.routers import DefaultRouter

#User.views
from cride.users.views import UserViewSet

router=DefaultRouter()
router.register(r'users',UserViewSet,basename="users")

urlpatterns=[
	path("",include(router.urls))
]