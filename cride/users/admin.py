# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#Models
from cride.users.models import User,Profile



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles' 



class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display=("email","username","first_name","last_name","is_verfied","is_client","is_active","is_staff","is_superuser")# Muestra info afuera
    search_fields=("username","first_name","last_name","email")# busqueda
    list_filter=("is_client","is_staff","created","modified")# filtro lateral
    date_hierarchy="created"

    fieldsets = (
        (None, {"fields": ("email","password")}), 
        ("Datos de usuario", {"fields": (("username",),("last_name", ),("first_name", ),("phone_number",))}),
        ("Permisos de clie",{"fields":(("is_verfied",),("is_client",))}),
        ("Permisos de administrador", {"fields": (("is_active", ),("is_staff", ),("is_superuser",),("groups"),("user_permissions"))}),     
        ("Metadata", {"fields": ("modified","created")}),
        )
    readonly_fields = ("created", "modified")  #Valores que no se podrán modificar



   
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","reputation","rides_taken","rides_offered","created")# Muestra info afuera
    search_fields=("user__username","user__email","user_first_name","user_last_name")# busqueda
    list_filter=("reputation","created","modified")# filtro lateral
    date_hierarchy="created"

    fieldsets = ((
        "Datos de perfil", {
            "fields": (("user","picture",), ("biography", ))
            }), 
        ("Datos extra", {
            "fields": (("rides_taken", ),("rides_offered", ),("reputation",))
            }), 
        ("Metadata", {
            "fields": ("created","modified",)
            })
        )
    readonly_fields = ("created", "modified")  #Valores que no se podrán modificar

admin.site.register(User,CustomUserAdmin)