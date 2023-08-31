# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ChangeForm, RegistrationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = ChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",
                    "first_name", "last_name", "mobile")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name", "email", "password1", "password2", "mobile", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
