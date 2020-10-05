# Django
from django.contrib import admin

#Models
from cride.circles.models import Circle,Membership,Invitation

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display=("name","slug_name","is_public","verified","is_limit","members_limit")# Muestra info afuera
    list_filter=("is_public","verified","is_limit","modified")# busqu
    date_hierarchy="created"


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass